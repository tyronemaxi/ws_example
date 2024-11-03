#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: tools.py
Time: 2024/11/3
"""
import json

from openai import OpenAI

from app.client.outer.weather import weather_cli, city_codes_cli
from conf.settings import OPENAI_API_KEY, OPENAI_API_BASE


def weather(query: str):
    """
    获取天气
    """
    city_code = city_codes_cli.get_adcode("苏州吴中")
    resp = weather_cli.get_weather(city_code)

    return resp


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据城市名，获取当地的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def get_completion(messages, model):
    client = OpenAI(base_url=OPENAI_API_BASE,
                    api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024,
        tools=tools
    )

    return response.choices[0].message


def chat(prompt, model='gpt-4'):
    messages = [
        {"role": "system", "content": "你是一个天气查询助手"},
        {"role": "user", "content": prompt}
    ]

    resp = get_completion(messages, model)

    if (resp.content is None):
        resp.content = ""

    messages.append(resp)
    print(resp)

    while resp.tool_calls is not None:
        for tool in resp.tool_calls:
            args = json.loads(tool.function.arguments)
            print("参数", args)

            if tool.function.name == "get_weather":
                result = weather()



