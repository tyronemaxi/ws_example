#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: base.py
Time: 2024/10/15 09:12
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class BaseRequests(object):
    """
        request 基础类封装
        :param base_url: ip/域名
        :param is_retry: 是否开启重试
        :param retries: 重试次数
        :param backoff_factor: 重试间隔时间
    """
    def __init__(self, base_url: str, is_retry: bool = False, retries: int = 3, backoff_factor=0.5):
        self._base_url = base_url
        self._session = requests.session()
        if is_retry:
            retries = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(pool_connections=20, max_retries=retries)
        else:
            adapter = HTTPAdapter(pool_connections=20)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

    def get(self, path: str = "", **kwargs):
        url = self._base_url
        if path:
            url = self._base_url + path

        response = self._session.get(url, **kwargs)
        return response

    def post(self, path="", data=None, json=None, **kwargs):
        url = self._base_url
        if path:
            url = self._base_url + path

        response = self._session.post(url, data=data, json=json, **kwargs)
        return response

    def put(self, path, data=None, **kwargs):
        url = self._base_url
        if path:
            url = self._base_url + path

        response = self._session.put(url, data=data, **kwargs)
        return response

    def delete(self, path, **kwargs):
        url = self._base_url
        if path:
            url = self._base_url + path

        response = self._session.delete(url, **kwargs)
        return response
