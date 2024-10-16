#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: http_code.py
Time: 2024/10/15 09:57
"""
# HTTP 状态码
HTTP_100_CONTINUE = 100
HTTP_101_SWITCHING_PROTOCOLS = 101
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
HTTP_204_NO_CONTENT = 204
HTTP_205_RESET_CONTENT = 205
HTTP_206_PARTIAL_CONTENT = 206
HTTP_207_MULTI_STATUS = 207
HTTP_208_ALREADY_REPORTED = 208
HTTP_226_IM_USED = 226
HTTP_300_MULTIPLE_CHOICES = 300
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_303_SEE_OTHER = 303
HTTP_304_NOT_MODIFIED = 304
HTTP_305_USE_PROXY = 305
HTTP_306_RESERVED = 306
HTTP_307_TEMPORARY_REDIRECT = 307
HTTP_308_PERMANENT_REDIRECT = 308
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_402_PAYMENT_REQUIRED = 402
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_406_NOT_ACCEPTABLE = 406
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
HTTP_408_REQUEST_TIMEOUT = 408
HTTP_409_CONFLICT = 409
HTTP_410_GONE = 410
HTTP_411_LENGTH_REQUIRED = 411
HTTP_412_PRECONDITION_FAILED = 412
HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413
HTTP_414_REQUEST_URI_TOO_LONG = 414
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416
HTTP_417_EXPECTATION_FAILED = 417
HTTP_418_IM_A_TEAPOT = 418
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_423_LOCKED = 423
HTTP_424_FAILED_DEPENDENCY = 424
HTTP_426_UPGRADE_REQUIRED = 426
HTTP_428_PRECONDITION_REQUIRED = 428
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_501_NOT_IMPLEMENTED = 501
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503
HTTP_504_GATEWAY_TIMEOUT = 504
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
HTTP_507_INSUFFICIENT_STORAGE = 507
HTTP_508_LOOP_DETECTED = 508
HTTP_509_BANDWIDTH_LIMIT_EXCEEDED = 509
HTTP_510_NOT_EXTENDED = 510
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511

# API内部错误，以1101开头
RequestSuccess = 0
UnknownError = 1001
ParamCheckError = 1101
ParamTypeError = 1102
DataBaseError = 1103
DataExistsError = 1104
AccessDenied = 1105
RequestTimeout = 1106
ExternalServerError = 1107
InsideServerError = 1108
ServiceUnavailable = 1109
MethodNotAllowed = 1110
DataNotFound = 1111
DataUpdateError = 1112
DataChangeError = 1113
DataDelError = 1114
DataQueryFailed = 1115
ModelNameNotFound = 1116

# 权限问题，以1200开头
UserNotLogin = 1200
UserAccessTokenExpire = 1201
UserRefreshTokenExpire = 1202
PoorReputation = 1203
UserPermissionDeny = -1

# 角色错误，以1300开头
RoleNotExists = 1301
RoleNameExists = 1302
RoleChangeError = 1303
RoleDelError = 1304
RoleExistsError = 1305

MESSAGE = {
    RequestSuccess: {"message": "请求成功", "http_code": HTTP_200_OK},
    UnknownError: {"message": "未知错误", "http_code": HTTP_500_INTERNAL_SERVER_ERROR},
    # API内部错误，以1101开头
    ParamCheckError: {"message": "参数错误", "http_code": HTTP_200_OK},
    ParamTypeError: {"message": "数据格式不正确", "http_code": HTTP_400_BAD_REQUEST},
    DataBaseError: {"message": "数据库错误", "http_code": HTTP_400_BAD_REQUEST},
    DataExistsError: {"message": "数据已存在", "http_code": HTTP_200_OK},
    DataQueryFailed: {"message": "数据查询失败", "http_code": HTTP_200_OK},
    AccessDenied: {"message": "请求被拒绝", "http_code": HTTP_403_FORBIDDEN},
    RequestTimeout: {"message": "等待超时", "http_code": HTTP_408_REQUEST_TIMEOUT},
    PoorReputation: {"message": "您目前信用分过低，禁止登录，请联系管理员", "http_code": HTTP_200_OK},
    ExternalServerError: {"message": "外部服务异常", "http_code": HTTP_500_INTERNAL_SERVER_ERROR},
    InsideServerError: {"message": "内部服务异常", "http_code": HTTP_500_INTERNAL_SERVER_ERROR},
    ServiceUnavailable: {"message": "接口异常，请稍后再试", "http_code": HTTP_503_SERVICE_UNAVAILABLE},
    MethodNotAllowed: {"message": "方法不允许", "http_code": HTTP_405_METHOD_NOT_ALLOWED},
    DataNotFound: {"message": "资源不存在", "http_code": HTTP_200_OK},
    DataUpdateError: {"message": "资源更新失败", "http_code": HTTP_200_OK},
    DataChangeError: {"message": "资源修改失败", "http_code": HTTP_400_BAD_REQUEST},
    DataDelError: {"message": "资源删除失败", "http_code": HTTP_400_BAD_REQUEST},
    ModelNameNotFound: {"message": "模型名称不存在", "http_code": HTTP_200_OK},
    # 用户错误，以1200开头
    UserNotLogin: {"message": "用户未登录，请扫码登录", "http_code": HTTP_200_OK},
    UserAccessTokenExpire: {"message": "AT 令牌过期，请重新获取", "http_code": HTTP_200_OK},
    UserRefreshTokenExpire: {"message": "RK 令牌不存在或已失效，请重新登录", "http_code": HTTP_200_OK},
    UserPermissionDeny: {"message": "用户权限不足", "http_code": HTTP_403_FORBIDDEN},

    RoleNotExists: {"message": "角色不存在", "http_code": HTTP_403_FORBIDDEN},
    RoleNameExists: {"message": "角色名已存在", "http_code": HTTP_403_FORBIDDEN},
    RoleChangeError: {"message": "角色修改失败", "http_code": HTTP_403_FORBIDDEN},
    RoleDelError: {"message": "角色删除失败", "http_code": HTTP_403_FORBIDDEN},
    RoleExistsError: {"message": "角色存在相关用户", "http_code": HTTP_403_FORBIDDEN},
}
