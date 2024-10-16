#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: time.py
Time: 2023/9/26
"""
import datetime

from conf.settings import TZ


def now_tz_datetime():
    """获取带TIMEZONE的datetime"""
    return datetime.datetime.now(tz=TZ)


def strftime(date: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M:%S"):
    return date.strftime(fmt)


def now_tz_datestring(fmt: str = "%Y-%m-%d"):
    return strftime(now_tz_datetime(), fmt=fmt)


def iso_datetime():
    now = datetime.datetime.now(tz=TZ)
    return now.isoformat()


if __name__ == '__main__':
    print(iso_datetime())