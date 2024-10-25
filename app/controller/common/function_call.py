#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: function_call.py
Time: 2024/10/25 14:30
"""
import openai
from openai import OpenAI
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

from conf.settings import OPENAI_API_KEY, OPENAI_API_BASE


class FunctionCall(object):
    def get_adcode(self):
        """
        获取城市区代码
        :return:
        """


    def get_weather(self):
        """
        获取实时天气
        :return:
        """
        pass


tools = FunctionCall()


