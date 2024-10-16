#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: healthcheck.py
Time: 2024/10/15 13:20
"""
from flask_restful import Resource

from app.core.response import ResUtil


class HealthCheckResource(Resource, ResUtil):
    def get(self):
        return self.message()
