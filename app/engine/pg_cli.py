#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: pg_cli.py
Time: 2024/10/15 10:23
"""
import time
import typing
from typing import Callable

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.query import Query
from sqlalchemy import text

from conf.settings import DB_HOST, DB_PORT, DB_USER, DB_DATABASE, DB_PASSWORD, SQL_PRINT
from app.core.log import logger

if typing:
    from sqlalchemy.engine.cursor import Result

engine = create_engine(
    url=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}',
    pool_recycle=300,
    pool_size=10,
    max_overflow=10,
    pool_timeout=30,
    echo=SQL_PRINT)


session = scoped_session(sessionmaker(bind=engine, future=True, autocommit=False, autoflush=False))


def pg_init():
    try:
        for i in range(3):
            session.execute(text("SELECT version()"))
            time.sleep(0.5)
    except Exception as e:
        logger.error(f"[Postgres] Cannot connect to Postgres, HOST: {DB_HOST}, PORT: {DB_PORT}, USER: {DB_USER},"
                     f" PWD: {DB_PASSWORD}, DB: {DB_DATABASE}, ERROR: {e}")
        # raise Exception(f"[Postgres] Cannot connect to Postgres for Error: {e}")
    else:
        logger.info(f"[PG] postgresql server HOST: {DB_HOST}, PORT: {DB_PORT} already connected")


def session_remove_wrap(func: Callable):
    def wrap(*args, **kwargs):
        if session.is_active:
            session.remove()
        res = func(*args, **kwargs)
        session.remove()
        return res

    return wrap


def execute_col(result: Result):
    # 获取查询的列名 原生的 sql
    return {column: value for column, value in zip(result.keys(), next(result, []))}


def query_col(query: Query):
    """
    查询字段并转换为[{data1}, {data2}...]
    只可在查询对象为字段时使用
    """

    return [dict(zip(v._mapping, v)) for v in query.all()]


def query_col_first(query: Query):
    """
    取第一条数据
    """
    data = query.first()

    if data:
        return dict(data._mapping)

    return {}


def pagination(query: Query, page: int = 1, per_page: int = 20):
    """
    Paginate a SQLAlchemy Query object.

    :param query: SQLAlchemy Query object.
    :param page: Page number, starting from 1.
    :param per_page: Number of items per page (default is 20).
    """
    pager_info = {}

    if page < 1:
        # If page is less than 1, return an empty result
        return [], pager_info

    count = query.count()
    max_page = (count + per_page - 1) // per_page
    if max_page < 1:
        return [], pager_info
    if page > max_page:
        page = max_page
    query = query.limit(per_page).offset((page - 1) * per_page)
    result = query_col(query)

    pager_info["page"] = page
    pager_info["per_page"] = per_page
    pager_info["total"] = count
    pager_info["pages"] = max_page

    return result, pager_info


def scroll_pagination(query: Query, offset: int = 0, limit: int = 0):
    """
    滚动分页
    :param query: 查询
    :param offset: 偏移量
    :param limit: 限制
    """
    pager_info = {}

    count = query.count()
    query = query.limit(limit).offset(offset-1)
    result = query_col(query)

    next_offset = offset + len(result)

    pager_info["offset"] = offset
    pager_info["limit"] = limit
    pager_info["next"] = next_offset
    pager_info["is_scroll"] = len(result) == limit
    pager_info["total"] = count

    return result, pager_info

