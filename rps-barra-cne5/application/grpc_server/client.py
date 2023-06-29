#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author: iamusera
    @date: 2023-04-21 14:35
    @description: 测试调用server的服务
"""
import grpc
import simplejson

import proto_buf.BarraRpcService_pb2 as pb2
import proto_buf.BarraRpcService_pb2_grpc as pb2_grpc


def oneway_streaming_request():
    """ 单向流式请求 """
    param = {
        "tables": ["df_trade_dt"],
        "start": "20230523",
        "end": "20230524"
    }
    req = pb2.BarraRequest(code="/cache/init_cache", json=simplejson.dumps(param))
    with grpc.insecure_channel('127.0.0.1:5001') as channel:
        stub = pb2_grpc.BarraRpcServiceStub(channel)
        r = stub.Barra(req)
        for ii in r:
            print(ii)


if __name__ == '__main__':
    oneway_streaming_request()
