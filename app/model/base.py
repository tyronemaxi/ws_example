#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: base.py
Time: 2024/10/15 10:38
"""
from typing import Any

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Boolean
from flask import g

from utils.time import now_tz_datetime

Base = declarative_base()


def get_attr_from_g(name: str, default: Any = None, raise_exception: bool = False):
    """
    从g对象中获取默认参数
    """

    def getter():
        try:
            if not hasattr(g, name):
                if raise_exception:
                    raise AttributeError("flask g has not attribute {name}")
                return default
            return getattr(g, name)
        except RuntimeError:
            return default

    return getter


class BaseModel(Base):
    """基类表模板"""
    __abstract__ = True

    create_time = Column(DateTime, nullable=False, default=now_tz_datetime, comment="创建时间")
    update_time = Column(DateTime, nullable=False, default=now_tz_datetime, onupdate=now_tz_datetime,
                         comment="修改时间")
    deleted_time = Column(DateTime, nullable=True, comment="删除时间")
    is_deleted = Column(Boolean, nullable=False, default=False, comment="是否已删除")

    def to_dict(self, keys=None):
        if keys:
            return {c: getattr(self, c, None) for c in keys}
        else:
            return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}