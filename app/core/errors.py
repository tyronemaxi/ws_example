#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: errors.py
Time: 2023/9/22
"""
import json
import traceback

from flask import Flask, jsonify, make_response
from flask import request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.exception import ApiError
from app.core import http_code as status
from app.core.log import logger
from app.core.response import ResUtil

err_code = -1  # TODO 暂时使用 -1 代替，后续使用 http code
ERROR_MESSAGE = "服务器内部错误，请联系管理员解决"


def record_error_log(func):
    """错误日志记录装饰器"""

    def log_func(err: Exception):
        r = func(err)
        if isinstance(r, tuple):
            # string response
            response_data = r[0]
            status_code = r[1]
        else:
            # json response
            response_data = r.json
            status_code = r.status_code

        # 避免因日志捕获 request body 错误, 而导致异常
        request_data = request.args if request.method == 'GET' else request.get_json(silent=True)
        err_data = json.dumps({
            "url": request.url,
            "remote_addr": request.remote_addr,
            "request_headers": dict(request.headers),
            "request_data": request_data,
            "response_data": response_data,
            "status_code": status_code
        }, ensure_ascii=False)

        logger.exception(err_data)
        return r

    return log_func


def register_error_handler(app: Flask):
    @app.errorhandler(status.HTTP_400_BAD_REQUEST)
    @record_error_log
    def catch_400_error(err: Exception):
        """捕捉400错误，常见于flask_restful.reparser参数解析失败"""
        message = None
        # 调整flask_restful.reparser的错误提示从dict转为默认str
        if isinstance(err, HTTPException):
            if getattr(err, "data", None) is None:
                return ResUtil.message(code=status.ParamCheckError, message=str(err))
            if isinstance(err.data.get("message"), dict):
                err_data = err.data["message"].popitem()
                message = "{error_name}: [{err_key}] -- {err_value}".format \
                    (error_name=err.name, err_key=err_data[0], err_value=err_data[1])

        return ResUtil.message(code=err_code, message=message)

    @app.errorhandler(status.HTTP_404_NOT_FOUND)
    @record_error_log
    def catch_404_error(err: Exception):
        """捕捉404错误"""
        return "<h2>{code} {name}</h2>\n{desc}".format(code=err_code, name=err.name, desc=err.description), status.HTTP_404_NOT_FOUND

    @app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
    @record_error_log
    def catch_405_error(err: Exception):
        """捕捉405错误，常见于url无该方法"""
        return ResUtil.message(code=err_code, message=str(err))

    @app.errorhandler(SQLAlchemyError)
    @record_error_log
    def catch_sqlalchemy_error(err: Exception):
        """捕获数据库/sql执行异常"""
        logger.error(str(err))
        return ResUtil.message(code=err_code, message="数据库异常,详细信息请查看业务后端日志")

    @app.errorhandler(Exception)
    @record_error_log
    def catch_other_error(err: Exception):
        """
        捕捉其他类型错误，返回相关错误信息
        """
        # 获取异常的堆栈跟踪信息
        traceback_info = traceback.format_exc()

        # 创建包含堆栈跟踪信息的消息
        error_message = f"{str(err)}\n{traceback_info}"

        return ResUtil.message(code=err_code, message=ERROR_MESSAGE)

    @app.errorhandler(ApiError)
    @record_error_log
    def catch_other_error(err: ApiError):
        """
        捕捉其他类型错误，返回相关错误信息
        """
        return make_response(
            jsonify({
                "code": err.code,
                "status": err.http_code,
                "message": err.message,
                "data": {}
            }), err.http_code)
