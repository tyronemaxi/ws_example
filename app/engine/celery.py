#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: celery.py
Time: 2024/10/16 10:09
"""
from celery import Celery

from conf.settings import TZ, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, CELERY_BROKER_DB

# 创建 Celery 实例
celery_app = Celery(
    broker_url=f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CELERY_BROKER_DB}",
    result_backend=f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CELERY_BROKER_DB}",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=TZ,
    enable_utc=False
)