from rest_framework import permissions
from base import models
import logging

logger = logging.getLogger('django')


class UserLoginRequire(permissions.BasePermission):
    """
    需要登录权限
    """

    def has_permission(self, request, view):
        # 传递token才可以访问
        auth_token = request.META.get('HTTP_X_USER_TOKEN', None)
        if not auth_token:
            return False
        try:
            user = models.User.objects.get(token=auth_token)
        except models.User.DoesNotExist:
            logger.error('UserLoginRequire:令牌对应的用户不存在')
            return False
        return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class AllowAny(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
