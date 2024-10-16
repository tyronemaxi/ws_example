#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: __init__.py
Time: 2024/10/15 09:11
"""
from flask import Flask

from .cors import cors_init

from app.engine import pg_cli, redis_cli


def register_extension(app: Flask):
    """
    注册扩展
    :param app:
    :return:
    """
    cors_init(app)
    pg_cli.pg_init()
    redis_cli.redis_init()