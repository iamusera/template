#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 15:27
    @description: celery模块
"""
from __future__ import absolute_import

from celery import Celery


def make_celery():
    c = Celery('celery_worker', include=['application.view.predict_mod.controller'])
    c.config_from_object("celery_app.config")

    return c


def init_celery(app, celery_):
    """
        initial celery object wraps the task execution in an application context
        """
    celery_.conf.update(app.config)
    task_base = celery_.Task

    class ContextTask(celery_.Task):
        def __call__(self, *args, **kwargs):
            abstract = True
            with app.app_context():
                # return task_base.__call__(self, *args, **kwargs)
                return task_base.__call__(self, *args, **kwargs)

    # setattr(celery_, 'Task', ContextTask)
    celery_.Task = ContextTask
    return celery_


celery_app = make_celery()
