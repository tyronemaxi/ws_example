#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: cors.py
Time: 2024/10/15 10:50
"""
from flask import Flask
from flask_cors import CORS

# 跨域配置
cors = CORS(resources=r"/*", supports_credentials=True, origins="*")


def cors_init(app: Flask):
    cors.init_app(app)