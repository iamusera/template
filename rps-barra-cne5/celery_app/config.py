#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 17:43
    @description: 
"""
BROKER_URL = 'redis://:biz@192.168.200.213:6379/1'
CELERY_RESULT_BACKEND = 'redis://:biz@192.168.200.213:6379/1'
CELERY_TASK_RESULT_EXPIRES = 60
