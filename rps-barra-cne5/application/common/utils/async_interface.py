#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 14:23
    @description: 
"""

from flask import has_request_context, copy_current_request_context
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor
import asyncio


def run_async(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        call_result = Future()

        def _run():
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
            except Exception as error:
                call_result.set_exception(error)
            else:
                call_result.set_result(result)
            finally:
                loop.close()

        loop_executor = ThreadPoolExecutor(max_workers=1)
        if has_request_context():
            _run = copy_current_request_context(_run)
        loop_future = loop_executor.submit(_run)
        loop_future.result()
        return call_result.result()

    return _wrapper
