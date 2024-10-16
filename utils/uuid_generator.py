#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: uuid_generator.py
Time: 2024/10/15 10:40
"""
import re
import uuid
import base64


# 获取压缩成22位的UUID
def compress_uuid(prefix: str) -> str:
    """
         uuid 生成器
        : param prefix 前缀
    """
    origin = str(uuid.uuid4()).replace('-', '')
    # return base64.b64encode(uuid.UUID(uuidstring).bytes).decode().rstrip('=\n')
    # url safe
    _uuid = base64.urlsafe_b64encode(uuid.UUID(origin).bytes).decode().rstrip('=\n')
    uuid_str = f"{prefix}_{_uuid}"
    return uuid_str