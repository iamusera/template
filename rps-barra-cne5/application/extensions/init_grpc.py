#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author: iamusera
    @date: 2023-04-26 15:36
    @description: 
"""
import grpc
from concurrent import futures
import application.grpc_server.proto_buf.BarraRpcService_pb2_grpc as pb2_grpc
from application.grpc_server.server import BarraRpcService


def init_grpc(app):
    url = "{}:{}".format(
                         app.config.get('RPC_HOST'),
                         app.config.get('RPC_PORT')
                         )
    rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(app.config.get('RPC_WORKER'))),
                             options=[('grpc.max_send_message_length', 1000 * 1024 * 1024),
                                      ('grpc.max_receive_message_length', 1000 * 1024 * 1024),
                                      ('grpc.timeout', 18000)],
                             )
    pb2_grpc.add_BarraRpcServiceServicer_to_server(BarraRpcService(app), rpc_server)
    rpc_server.add_insecure_port(url)
    rpc_server.start()
    # logger.info(f" * gRPC service start on {url}")
    print(f" * gRPC service start on {url}")
    app.grpc_server = rpc_server
