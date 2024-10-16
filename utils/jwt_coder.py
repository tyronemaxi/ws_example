#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: jwt_coder.py
Time: 2024/10/16 10:53
"""
import jwt
from jwt.exceptions import ExpiredSignatureError
import datetime

from conf.settings import SECRET_KEY, JWT_AUTH_VERSION
from app.core.log import logger


class JWTCoderBase(object):
    """
    jwt 生成解析基础类，用于扩展，方便逻辑修改，后续逻辑发生变化，可继承修改。遵守开闭原则
    """
    @staticmethod
    def parse_jwt_token(token: str, verify_signature: bool = True):
        """
        :param verify_signature: 是否校验签名
        :param token: 待解析的 token 串
        :return:
        """
        err_code = None
        payload = {}
        try:
            if verify_signature:
                payload = jwt.decode(token, key=SECRET_KEY, algorithms="HS256")
            else:
                payload = jwt.decode(token, key=SECRET_KEY, algorithms="HS256",
                                     options={"verify_signature": False})

        except ExpiredSignatureError as e:
            # jwt 过期
            logger.error(f"[Auth] jwt 过期，error: {e}")
            err_code = 1
        except Exception as e:
            err_code = 2
            logger.error("认证信息有误，请重新登陆，err: {}".format(e))

        return payload, err_code

    @staticmethod
    def generate_access_token(user_info: dict, user_type: int, hours: int):
        """
        生成 jwt token
        """
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }

        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)

        payload = {
            "version": JWT_AUTH_VERSION,  # TODO 保留字段，用于后期 token 主动过期
            "user_type": user_type,
            "last_exp": int(datetime.datetime.utcnow().timestamp()),  # 记录本次的 token 颁发时间
            "exp": exp
        }

        payload.update(user_info)

        logger.debug(f"user_info: {payload}")
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256", headers=headers)

        return token


jwt_corder = JWTCoderBase()
