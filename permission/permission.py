from rest_framework.permissions import BasePermission
from .verify import verify_permission


class IsCasBinVerify(BasePermission):
    def has_permission(self, request, view):
        path = request.META["PATH_INFO"]
        username = request.user.username
        method = request.method
        return verify_permission(username, path, method)
