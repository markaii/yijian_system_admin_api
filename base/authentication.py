import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from base import models

logger = logging.getLogger('django')


class DummyAuthentication(BaseAuthentication):
    def authenticate_header(self, request):
        super().authenticate_header(request)

    def authenticate(self, request):
        pass


class UserTokenAuthentication(BaseAuthentication):
    """
    客户Token验证
    校验客户请求时候的Token，面向h5端
    """

    def authenticate_header(self, request):
        super(UserTokenAuthentication, self).authenticate_header(request)

    def authenticate(self, request):
        auth_token = request.META.get('HTTP_X_USER_TOKEN', None)
        print(request)
        if not auth_token:
            raise AuthenticationFailed('HTTP-X-USER-TOKEN不能为空')
        try:
            user = models.User.objects.get(token=auth_token)
        except models.User.DoesNotExist:
            logger.error('UserTokenAuthentication:用户不存在 :' + auth_token)
            raise AuthenticationFailed('用户不存在')
        return user, auth_token
