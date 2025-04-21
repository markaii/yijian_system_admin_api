import logging
from django.db import DatabaseError
from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.utils import serializer_helpers

from common.exceptions import LogicalError
from common.response import JsonResponse
from common import exceptions

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    logger.debug('custom_exception_handler')
    logger.debug(response)
    # 系统其它的异常
    if isinstance(exc, DatabaseError):
        logger.debug(exc)
        return JsonResponse(code=500, message='数据库异常请联系管理员', data=str(exc), status=500)
        # exc = exceptions.DatabaseServiceError()  # 数据库错误，无法连接，表不存在等等
    if isinstance(exc, Http404):
        return JsonResponse(code=404, message='未找到您查询的数据', data=str(exc), status=404)
    # 这里的出错处理有两种情况
    # 1. 系统错误：需要处理 status_code，需要处理detail和message
    # 方法不允许 {"detail": "Method 'DELETE' not allowed."}
    # 系统校验 {"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
    # 2. 业务错误：status_code是自定义的，http status code和code都要设置，其中status_code 和 code（业务代号）
    if response is not None:
        # print(type(exc.detail))
        if exc.detail:
            message = exc.detail
        else:
            message = exc.default_detail
        if isinstance(exc, exceptions.LogicalError):
            logger.debug(message)
            return JsonResponse(code=exc.code,
                                message='{} {}'.format(exc.code, message),
                                data=exc.data,
                                status=response.status_code)
        if isinstance(exc.detail, exceptions.exceptions.ErrorDetail):
            print(message)
            logger.debug(message)
            return JsonResponse(code=response.status_code,
                                message='{} {}'.format(response.status_code, message),
                                data=None,
                                status=response.status_code)
        if isinstance(exc.detail, serializer_helpers.ReturnDict):
            print(exc.default_detail)
            logger.debug(exc.default_detail)
            print(exc.detail)
            logger.debug(exc.detail)
            return JsonResponse(code=response.status_code,
                                message='{} {}'.format(response.status_code, exc.default_detail),
                                data=exc.detail,
                                status=response.status_code)
    # 其他的系统级别的错误我们直接跑出去
    print(exc)
    logger.debug(exc)
    return JsonResponse(code=500, message='未知错误请联系管理员', data=str(exc), status=500)
