#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: events.py
Time: 2024/12/9 13:49
"""
from flask import g
from flask_socketio import emit, send, join_room
from flask import request
from enum import Enum

from app.core.log import logger
from .auth import auth


class Events(object):
    @auth()
    def connect(self):
        # 连接 && auth
        user_id = g.user_id
        join_room(room=user_id)
        emit('message', {"data": "connected"}, room=user_id)

    def start_session(self):
        pass

    # 监听客户端发送的普通消息
    def handle_message(self, message):
        print('Received message:', message)
        send('Hello from server')

    def end_session(self):
        pass

    def disconnect(self):
        pass


events = Events()
