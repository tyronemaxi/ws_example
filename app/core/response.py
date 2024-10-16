#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: response.py
Time: 2024/10/15 09:57
"""
from flask import jsonify, g
from typing import Any
from .http_code import *


class ResUtil(object):
    """作为resource中的扩展类使用"""

    @property
    def user_id(self):
        return getattr(g, "user_id", None)

    @user_id.setter
    def user_id(self, value: str):
        g.user_id = value

    @property
    def user(self):
        return getattr(g, "user", None)

    @user.setter
    def user(self, value: dict):
        if self.user is None:
            g.user = value
        else:
            g.user.update(value)

    @property
    def headers(self):
        return getattr(g, "headers", None)

    @headers.setter
    def headers(self, value: dict):
        if self.headers is None:
            g.headers = value
        else:
            g.headers.update(value)

    @staticmethod
    def message(data: Any = None, code: int = 0, message: str = None, pager_info: dict = None, origin: Any = None):
        """
        标准API返回函数

        :param data: api回调数据
        :param code: 见 status_code
        :param message: 明文回调信息,会覆写预设信息
        :param pager_info: 分页信息
        :param origin: 无需封装直接返回,会忽略其他参数
        :return: 规范的json数据
        """
        if origin is not None:
            response = origin
            if "code" in origin and code in MESSAGE:
                http_code = MESSAGE[origin["code"]]["http_code"]
            else:
                http_code = 500
        else:
            if MESSAGE.get(code) is None:
                http_code = 403
                message = message
            else:
                http_code = MESSAGE[code]["http_code"]
                message = MESSAGE[code]["message"] if message is None else message

            response = {
                "code": code,
                "status": http_code,
                "msg": message,
                "data": {}
            }

            # 无数据模式
            if data is None:
                response["data"] = {}

            # 对象格式
            elif isinstance(data, dict):
                response["data"].update(data)

            # 列表格式
            elif isinstance(data, list):
                response["data"]["items"] = data
                if pager_info:
                    response["data"].update(pager_info)

            elif isinstance(data, str):
                response["data"] = data

            # 其他情况报错
            else:
                raise TypeError("unsupported response data format")

        resp = jsonify(response)
        resp.status_code = http_code

        return resp


res_util = ResUtil()
