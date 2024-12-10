#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: auth.py
Time: 2024/12/10 13:37
"""
from flask import request

from functools import wraps
from flask import g

from utils.jwt_coder import jwt_corder
from app.core.log import logger
from conf.settings import ENABLE_QW_LOGIN


def auth():
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            # 权限认证
            url = request.path
            client_ip = request.headers.get("X-Real-IP", request.remote_addr)

            g.client_ip = client_ip
            access_token = request.headers.get("access_token", "")
            logger.debug(f"[Auth] client ip: {client_ip}, access token: {access_token}")

            code = 0
            msg = {"message": "success"}
            if ENABLE_QW_LOGIN:
                # 需要登陆
                if access_token:
                    user_info, access_err_code = jwt_corder.parse_jwt_token(access_token)
                    if not access_err_code:
                        # 有效的 access_token
                        last_exp = int(user_info["last_exp"])
                        logger.debug(f"user_info: {user_info}, last_expire_time: {last_exp}")

                        g.client_ip = client_ip
                        g.user_info = user_info
                        g.user_id = user_info["user_id"]
                        return f(*args, **kwargs)

                    else:
                        # access_token 过期或失效
                        msg = {"message": "auth fail"}
                        code = 403
                        return msg, code

                else:
                    msg = {"message": "auth fail"}
                    code = 403
                    return msg, code

            else:
                msg = {"message": "auth fail"}
                code = 403
                return msg, code

        return inner

    return decorator
