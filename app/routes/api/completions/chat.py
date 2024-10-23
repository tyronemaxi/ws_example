#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: chat.py
Time: 2024/10/21
"""
from flask_restful import Resource
from flask import Response

from app.core.response import ResUtil, StreamResponseGen
from app.core.request import args_parser, fields, not_empty
from app.controller.completions.chat import chat_ctrl


class ChatResource(Resource, ResUtil):
    @args_parser({
        "query": fields(type=str, required=True, process=not_empty),
        "stream": fields(type=bool, default=True)
    })
    def post(self, query: str, stream: bool = True):
        gen = StreamResponseGen()
        conv_id = "123"
        cp_id = "234"
        user_id = "123456"
        chat_ctrl.run_async_task(gen, query, conv_id, cp_id, user_id, stream)

        return Response(gen, content_type='text/event-stream')
