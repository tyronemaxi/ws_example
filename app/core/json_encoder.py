#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: json_encoder.py
Time: 2023/9/22
"""
from datetime import date, time

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """修复datetime打印格式"""
    def default(self, obj):
        try:
            if isinstance(obj, (date, time)):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         return super().default(obj)