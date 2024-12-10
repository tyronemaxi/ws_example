#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: ws.py
Time: 2024/12/9 13:22
"""
from flask import Flask, request

from flask_socketio import SocketIO
from app.core.log import logger
from utils.jwt_coder import jwt_corder
from app.controller.ws.events import events

socketio = SocketIO(cors_allowed_origins='*', async_mode="gevent", manage_session=True)


def register_ws_event(app):
    socketio.init_app(app)

    # connect
    @socketio.on('connect')
    def connection():
        events.connect()

    @socketio.on_error_default
    def error_handler(e):
        messages = {
            "message": request.event["message"],
            "args": request.event["args"]
        }

        logger.debug(f"[ws] ws error for {e}, events: {messages}")

    @socketio.on('message')
    def handel_message(message):
        events.handle_message(message)

    return socketio
