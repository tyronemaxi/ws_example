#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: redis_cli.py
Time: 2023/11/3 1:51 PM
"""
import time

import redis

from conf.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_CACHE_DB
from app.core.log import logger

normal_cache_pool = redis.ConnectionPool(
                        host=REDIS_HOST, port=REDIS_PORT,
                        password=REDIS_PASSWORD, db=REDIS_CACHE_DB,
                        decode_responses=True)

r_cache = redis.StrictRedis(connection_pool=normal_cache_pool)


def redis_init():
    try:
        for i in range(3):
            time.sleep(0.5)
            r_cache.ping()
    except Exception as e:
        logger.error(f"Redis server: [{REDIS_HOST}:{REDIS_PORT}] not connected for e: {e}")
        # raise Exception("Redis is not connected of [{REDIS_HOST}:{REDIS_PORT}]")
    else:
        logger.info(f"Redis server: [{REDIS_HOST}:{REDIS_PORT}] connected")
