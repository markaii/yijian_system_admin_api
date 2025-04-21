from rest_framework import exceptions, status


# 系统级别的错误

class DatabaseServiceError(exceptions.APIException):
    status_code = 500
    default_detail = '数据库出错请稍后尝试'


class AuthenticationError(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '授权失败'


class ServerError(exceptions.APIException):
    status_code = 500
    default_detail = '系统错误请稍后尝试'


# 业务逻辑的错误


class ParamsError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '请求参数错误请检查'


class LogicalError(exceptions.APIException):
    code = '000000'
    status_code = 400  # 这是业务逻辑返回的http状态码
    default_detail = '业务逻辑异常'
    data = ''

    def __init__(self, message=None, code=None, status_code=None, data=None):
        super().__init__(message, code)
        if data is not None:
            self.data = data
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
