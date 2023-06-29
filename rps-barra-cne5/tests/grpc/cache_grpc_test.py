import unittest

import simplejson

from application import create_app
import grpc
import application.grpc_server.proto_buf.BarraRpcService_pb2 as pb2
import application.grpc_server.proto_buf.BarraRpcService_pb2_grpc as pb2_grpc


class MyTestCase(unittest.TestCase):
    def test_something(self):
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
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    create_app().run(debug=False, host='0.0.0.0')
    unittest.main()
