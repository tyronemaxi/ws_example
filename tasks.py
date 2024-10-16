#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: tasks.py
Time: 2024/10/16 10:21
"""
# celery 异步任务
from app.core.log import register_logger
from app.engine.pg_cli import session_remove_wrap
from app.engine.celery import celery_app

register_logger()


@celery_app.task(name='test_task', ignore_result=True)
@session_remove_wrap
def test_task():
    """
    示例代码
    :return:
    """
    ...
