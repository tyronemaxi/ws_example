#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: auth.py
Time: 2024/10/16 11:04
"""
from flask import request, g

from app.core.http_code import UserNotLogin
from app.core.log import logger
from conf.settings import ENABLE_QW_LOGIN
from utils.jwt_coder import jwt_corder
from app.core.response import ResUtil


def parse_token():
    url = request.path
    # 校验是否需要认证
    client_ip = request.headers.get("X-Real-IP", request.remote_addr)
    g.client_ip = client_ip
    access_token = request.headers.get("access_token", "")
    logger.debug(f"[Auth] client ip: {client_ip}, access token: {access_token}")

    return url, client_ip, access_token


def auth_handler():
    """
    权限认证
    :return:
    """

    url, client_ip, access_token = parse_token()

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
                return ResUtil.message(code=UserNotLogin)

            g.user_info = user_info
        else:
            return ResUtil.message(code=-1, message="access token 未传，请确认!")

    else:
        pass
