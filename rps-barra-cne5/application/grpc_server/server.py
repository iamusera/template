#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author: iamusera
    @date: 2023-04-21 14:29
    @description: 
"""
import time
from loguru import logger
import application.grpc_server.proto_buf.BarraRpcService_pb2 as pb2
import application.grpc_server.proto_buf.BarraRpcService_pb2_grpc as pb2_grpc
from application.grpc_server.request_resolver import request_resolve


class BarraRpcService(pb2_grpc.BarraRpcServiceServicer):
    def __init__(self, app):
        self.app = app

    def Barra(self, request_iterator: pb2.BarraRequest, context):
        """ 单向流式 """
        with self.app.app_context():
            try:
                logger.info(request_iterator)
                result = request_resolve(request_iterator.code, request_iterator.json)
                for e in iter(result):
                    print(f'finished! code: {e.code} message: {e.message}')
                    yield pb2.BarraResponse(code=e.code, message=e.message)
            except Exception as e:
                logger.exception(e)
            except:
                import traceback
                print(traceback.format_exc())
