from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model

from permission.models import Role


User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)  # 查询使用

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone",
                  "introduction", "department", "uid",
                  "is_staff", "is_active", "is_superuser", "date_joined", "role")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone", "password",
                  "introduction", "department", "uid",
                  "is_staff", "is_active", "is_superuser", "date_joined", "role")
        extra_kwargs = {
            "username": {
                "required": True,
                "help_text": "必填用户名"
            },
            "password": {
                "write_only": True,
                "style": {'input_type': 'password'},
                "help_text": "密码",
                "label": "密码1",
            },
            "email": {
                "required": True
            },
            "date_joined": {
                "read_only": True,
                "format": '%Y-%m-%d %H:%M'
            },
            "uid": {
                "read_only": True
            }
        }
        depth = 1


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "first_name", "last_name", "role")