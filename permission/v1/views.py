from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings

from ..models import RouterView, Role, CasBinPermissionRule, RoleBind
from .serializer import RouterSerializer, RoleSerializer, \
    PermissionRuleSerializer, RoleBindSerializer, RouterManagerSerializer, UserProfileSerializer

User = get_user_model()


# 前端用户获取访问路由
class Router(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        role_qs = request.user.role.all()
        for role in role_qs:
            if role.name == settings.ADMIN_ROLE:
                routers = self.get_queryset()
                serializer = RouterSerializer(routers, many=True)
                result = self.generate_routes(serializer.data)
                return Response(result)
        routers = self._get_roles_router(role_qs)
        serializer = RouterSerializer(routers, many=True)
        result = self.generate_routes(serializer.data)
        return Response(result)

    def _get_roles_router(self, roles):
        role_id = [r.rid for r in roles]
        return self.get_queryset().filter(role__rid__in=role_id)

    def get_queryset(self):
        return RouterView.objects.all()

    def generate_routes(self, data):
        def sub(node_id):
            current_node = _data(node_id)
            current_node["children"] = []
            for node in data:
                if node['parent'] == node_id:
                    current_node['children'].append(sub(node["id"]))
            else:
                return current_node

        def _data(pk):
            db_data = {node['id']: node for node in data}
            return db_data.get(pk)

        result = [sub(node["id"]) for node in data if node['isParent']]
        return result


# 路由管理
class RouterManager(ModelViewSet):
    serializer_class = RouterManagerSerializer
    queryset = RouterView.objects.all()
    lookup_field = 'router_id'

    def list(self, request, *args, **kwargs):
        routers = self.get_queryset()
        serializer = RouterSerializer(routers, many=True)
        result = self.generate_routes(serializer.data)
        return Response(result)

    def generate_routes(self, data):
        def sub(node_id):
            current_node = _data(node_id)
            current_node["children"] = []
            for node in data:
                if node['parent'] == node_id:
                    current_node['children'].append(sub(node["id"]))
            else:
                return current_node

        def _data(pk):
            db_data = {node['id']: node for node in data}
            return db_data.get(pk)

        return [sub(node["id"]) for node in data if node['isParent']]

    def perform_destroy(self, instance):
        instance.meta.delete()
        instance.delete()


# 角色
class RoleView(ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = 'rid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        related = get_role_related(instance)
        for res, values in related.items():
            if values:
                return Response("<{}>已绑定<{}>角色，不能删除".format(res, instance.name),
                                status=status.HTTP_400_BAD_REQUEST)

        return super(RoleView, self).destroy(request, *args, **kwargs)


# 查询角色反向关联
class RoleRelated(APIView):
    authentication_classes = []
    permission_classes = []

    def get_object(self, rid):
        role = Role.objects.all().filter(rid=rid)
        if role:
            return role[0]
        else:
            return None

    def get(self, request, rid, *args, **kwargs):
        role = self.get_object(rid)
        if not role:
            return Response("未找到对应角色", status=status.HTTP_404_NOT_FOUND)
        result = get_role_related(role)
        return Response(result)


# 权限规则, 角色对应的权限
class PermissionRuleView(ModelViewSet):
    serializer_class = PermissionRuleSerializer
    queryset = CasBinPermissionRule.objects.all()
    lookup_field = 'cid'


# casbin 用户和权限绑定
class PermissionRoleBindView(ModelViewSet):
    serializer_class = RoleBindSerializer
    queryset = RoleBind.objects.all()
    lookup_field = 'bid'


def get_role_related(role):
    result = {
        "user": [],
        "routerView": [],
        "permissionRule": [],
        "roleBind": []
    }

    # 用户 Role.objects.all()[0].user_profile.all()
    user_qs = role.user_profile.all()
    user = UserProfileSerializer(instance=user_qs, many=True)
    result['user'] = user.data

    # 前端路由视图 Role.objects.all()[0].router_view.all()
    router_qs = role.router_view.all()
    router_view = RouterSerializer(instance=router_qs, many=True)
    result['routerView'] = router_view.data

    # 权限规则 CasBinPermissionRule.objects.all().filter(role=Role.objects.all()[0].name)
    perm_rule_qs = CasBinPermissionRule.objects.all().filter(role=role.name)
    perm_rule = PermissionRuleSerializer(instance=perm_rule_qs, many=True)
    result['permissionRule'] = perm_rule.data

    # 权限绑定 RoleBind.objects.all().filter(role=Role.objects.all()[0].name)
    bind_qs = RoleBind.objects.all().filter(role=role.name)
    bind = RoleBindSerializer(instance=bind_qs, many=True)
    result['roleBind'] = bind.data
    return result
