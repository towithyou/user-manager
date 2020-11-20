# from rest_framework.utils import model_meta
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from permission.models import Role, RouterView, CasBinPermissionRule, RoleBind, RouterMeta
from users.models import UserProfile


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Role.objects.all(),
                fields=['name']
            )
        ]


class RouterMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterMeta
        fields = '__all__'


class RouterSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True)
    meta = RouterMetaSerializer(many=False)

    class Meta:
        model = RouterView
        fields = '__all__'


class RouterManagerSerializer(serializers.ModelSerializer):
    meta = RouterMetaSerializer(many=False)
    role = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())

    def validate(self, attrs):
        return attrs

    def _get_meta_obj(self, request):
        meta_data = request.data.get('meta')
        if not meta_data.get("id"):
            raise exceptions.ValidationError({
                "meta": "id主键更新必传"
            })
        meta_obj = RouterMeta.objects.filter(id=meta_data.get("id"))
        if not meta_obj:
            raise exceptions.ValidationError({
                "meta": "对象<{}>不存在".format(meta_data.get("id"))
            })

        return meta_obj[0]

    def update(self, instance, validated_data):
        # 更新 meta 数据
        request = self.context['request']
        meta_obj = self._get_meta_obj(request)
        update_meta = validated_data.pop("meta")
        for attr, value in update_meta.items():
            setattr(meta_obj, attr, value)
        meta_obj.save()

        # 更新角色
        role_objs = validated_data.pop('role')
        instance.role.set([r.id for r in role_objs])
        instance.save()
        return super(RouterManagerSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        meta_data = validated_data.pop('meta')
        role_objs = validated_data.pop('role')
        meta = RouterMeta.objects.create(**meta_data)

        # 创建并且save了, 必须指定meta
        router = RouterView.objects.create(meta=meta, **validated_data)

        if role_objs:
            router.role.add(*role_objs)  # PrimaryKeyRelatedField so 必须是主键id
        router.save()
        return router

    class Meta:
        model = RouterView
        fields = '__all__'
        extra_kwargs = {
            "router_id": {
                "read_only": True
            }
        }


class PermissionRuleSerializer(serializers.ModelSerializer):
    TYPE_CHOICES = (
        ('p', 'p'),
    )

    ptype = serializers.ChoiceField(choices=TYPE_CHOICES, required=True)
    role = serializers.CharField(required=True)
    path = serializers.CharField(required=True)
    method = serializers.CharField(required=True)

    def validate_role(self, val):
        if Role.objects.filter(name__exact=val):
            return val
        raise exceptions.ValidationError('<{}>角色名称不正确'.format(val))

    def validate_path(self, val: str):
        if val == "*":
            return val
        if val.endswith("*") and val.startswith('/'):
            return val
        if val.startswith('/') and val.endswith('/'):
            return val
        raise exceptions.ValidationError('<{}>路径不正确'.format(val))

    def validate_method(self, val: str):
        allowed_request_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        if val == "*":
            return val
        if val in allowed_request_methods:
            return val
        if val.startswith("(") and val.endswith(")"):
            return val
        raise exceptions.ValidationError('请求方法<{}>错误'.format(val))

    class Meta:
        model = CasBinPermissionRule
        exclude = ("v3", "v4")
        extra_kwargs = {
            "cid": {
                "read_only": True
            }
        }


class RoleBindSerializer(serializers.ModelSerializer):
    TYPE_CHOICES = (
        ('g', 'g'),
    )

    ptype = serializers.ChoiceField(choices=TYPE_CHOICES, required=True)
    username = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    def validate_role(self, val):
        if Role.objects.filter(name__exact=val):
            return val
        raise exceptions.ValidationError('<{}>角色名称不正确'.format(val))

    def validate_username(self, val):
        if UserProfile.objects.filter(username__exact=val):
            return val
        raise exceptions.ValidationError('<{}>用户名称不正确'.format(val))

    class Meta:
        model = RoleBind
        fields = '__all__'
        extra_kwargs = {
            "bid": {
                "read_only": True
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=RoleBind.objects.all(),
                fields=["username", "role"]
            )
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ("password", "first_name", "last_name", "groups", "user_permissions")