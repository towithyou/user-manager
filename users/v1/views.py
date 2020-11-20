from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model

from permission.models import Role
from .serializer import UserSerializer, UserProfileSerializer, UserUpdateSerializer

User = get_user_model()


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, *args, **kwargs):
        obj = requset.user
        serializer = UserProfileSerializer(obj, many=False)
        return Response(serializer.data)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'uid'

    def _get_roles(self, request):
        return Role.objects.filter(rid__in=request.data.get("role", []))

    def _get_pwd(self, request):
        return request.data.get("password", "")

    def create(self, request, *args, **kwargs):
        roles = self._get_roles(request)
        pwd = self._get_pwd(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(id=serializer.data['id'])
        if pwd:
            user.set_password(pwd)
        user.set_password(pwd)
        if roles:
            user.role.add(*roles)
        else:
            Response({"role": "角色不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        s = self.get_serializer(instance=user)
        return Response(s.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        roles = self._get_roles(request)
        pwd = self._get_pwd(request)
        partial = True if request.method == "PATCH" else False

        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        user = User.objects.get(id=serializer.data['id'])
        if pwd:
            user.set_password(pwd)
        if roles:
            user.role.set([r.id for r in roles])
        else:
            Response({"role": "角色不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        s = self.get_serializer(instance=user)
        return Response(s.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.username == "admin":
            return Response("默认admin用户不能删除", status=status.HTTP_400_BAD_REQUEST)
        return super(UserView, self).destroy(request, *args, **kwargs)
