from application.exception import ApiException


class ServerError(ApiException):
    code = 500
    msg = "server is invallid"
    data = ''


class ClientTypeError(ApiException):
    code = 400
    msg = "client is invallid"
    data = ''


class ParameterException(ApiException):
    code = 400
    msg = 'invalid parameter'
    data = ''


class AuthFailed(ApiException):
    code = 401
    msg = 'invalid parameter'
    data = ''


class ValError(ApiException):
    code = 404
    msg = 'invalid parameter'
    data = ''
