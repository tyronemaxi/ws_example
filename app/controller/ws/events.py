#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: events.py
Time: 2024/12/9 13:49
"""
from flask import g
from flask_socketio import emit
from flask import request
import json

from app.core.log import logger
from app.core.response import ResUtil
from conf.settings import ENABLE_QW_LOGIN
from app.core.http_code import UserNotLogin
from utils.jwt_coder import jwt_corder


class Events(object):
    def connect(self):
        # data = self.auth()
        data = {"message": "connected success"}
        # logger.info(f"user: {g.user_id} connected!")
        # data = ResUtil.message(message="connected to ws server")
        emit("data", json.dumps(data))

    def auth(self):
        """
        jwt 权限认证
        """
        url, client_ip, access_token = self._parse_token()

        if ENABLE_QW_LOGIN:
            # 需要登陆
            if access_token:
                user_info, access_err_code = jwt_corder.parse_jwt_token(access_token)
                if not access_err_code:
                    # 有效的 access_token
                    last_exp = int(user_info["last_exp"])
                    user_type = user_info["user_type"]
                    logger.debug(f"user_info: {user_info}, last_expire_time: {last_exp}")

                    g.client_ip = client_ip
                    g.user_info = user_info
                    g.user_id = user_info["user_id"]

                else:
                    # access_token 过期或失效
                    return {"msg": "need auth token"}

                g.user_info = user_info
            else:
                return {"msg": "acquire token"}

        else:
            pass

    @staticmethod
    def _parse_token():
        url = request.path
        # 校验是否需要认证
        client_ip = request.headers.get("X-Real-IP", request.remote_addr)
        g.client_ip = client_ip
        access_token = request.headers.get("access_token", "")
        logger.debug(f"[Auth] client ip: {client_ip}, access token: {access_token}")

        return url, client_ip, access_token

    def start_session(self):
        pass

    def start_task(self):
        pass

    def end_session(self):
        pass

    def disconnect(self):
        pass

events = Events()
