#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: middleware.py
Time: 2024/10/15 10:10
"""
import os


from flask import Flask

from app.engine.pg_cli import session as pg_session
from .auth import auth_handler

dir_name = os.path.dirname(__file__)


def register_middleware(app: Flask) -> None:
    """
    注册中间件
    """
    # @app.before_request
    # def auth():
    #     return auth_handler()

    # @app.teardown_request
    # def shutdown_session(exception=None):
    #     pg_session.remove()
