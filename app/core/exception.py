#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: exception.py
Time: 2024/10/15 09:59
"""
from app.core.http_code import UnknownError, MESSAGE
from app.core.http_code import ParamCheckError, DataNotFound
from app.core.http_code import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class ApiError(Exception):
    """
    标准 API 异常
    """
    default_message = "服务端异常"
    default_code = UnknownError
    default_http_code = MESSAGE[default_code]["http_code"]

    def __init__(self, code=None, message=None, http_code=None, *args, **kwargs):
        """
        标准 API 异常构造函数

        :param code: 异常编码
        :param msg: 异常信息
        :param args:
        :param kwargs:
        """
        super(ApiError, self).__init__(code, message, *args)

        self.code = code or self.default_code
        self.message = message or self.default_message
        self.http_code = http_code or MESSAGE.get(self.code, {}).get("http_code") or self.default_http_code
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return f"""{self.__class__.__name__}(code={self.code}, message={self.message}, http_code={self.http_code})"""

    @property
    def data(self):
        result = {
            "code": self.code,
            "message": self.message,
            "http_code": self.http_code
        }

        result.update(self.kwargs)
        return result


class NotFoundError(ApiError):
    default_code = DataNotFound
    default_message = "数据不存在"
    default_http_code = HTTP_404_NOT_FOUND


class ParamsCheckError(ApiError):
    default_code = ParamCheckError
    default_message = "参数校验失败"
    default_http_code = HTTP_400_BAD_REQUEST