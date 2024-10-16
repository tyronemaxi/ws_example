#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: flask_config.py
Time: 2023/9/22
"""
import datetime
from flask import Config
from conf.settings import SECRET_KEY, SQL_PRINT


class BasicConfig(Config):
    SECRET_KEY = SECRET_KEY
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(
    BasicConfig,
):
    ENV = "development"
    DEBUG = True


class SitConfig(
    BasicConfig
):
    ENV = "sit"
    DEBUG = True


class UatConfig(
    BasicConfig
):
    ENV = "uat"
    DEBUG = False


class ProductionConfig(
    BasicConfig
):
    ENV = "production"
    DEBUG = False


Configs = {
    "dev": DevelopmentConfig,
    "sit": SitConfig,
    "uat": UatConfig,
    "prod": ProductionConfig
}
