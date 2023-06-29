#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-03-06 15:49
    @description: 
"""
import os
from loguru import logger

def init_log(app):
    info_ = app.config.get('INFO_LOG')
    error_ = app.config.get('ERROR_LOG')
    
    logger.add(
        info_.get('file'),
        level=info_.get('level'),
        colorize=info_.get('colorize'),
        enqueue=info_.get('enqueue'),
        format=info_.get('format'),
        rotation=info_.get('rotation'),
        retention=info_.get('retention')
    )
    logger.add(
        os.path.abspath(error_.get('file')),
        level=error_.get('level'),
        colorize=error_.get('colorize'),
        enqueue=error_.get('enqueue'),
        format=error_.get('format'),
        rotation=error_.get('rotation'),
        retention=error_.get('retention')
    )