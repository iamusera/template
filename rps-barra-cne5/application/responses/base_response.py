#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 13:18
"""
import simplejson


class BaseResponse:
    code = ''
    data = []
    message = ""

    def __init__(self,
                 code=None,
                 data=None,
                 message=None,
                 ):
        self.result_dic = dict()
        self.result_dic["message"] = self.message if message is None else message
        self.result_dic["data"] = self.data if data is None else data
        self.result_dic["code"] = self.code if data is None else code

    def result(self):
        return simplejson.dumps(self.result_dic, ensure_ascii=False, ignore_nan=True, indent=True)


class SuccessResponse(BaseResponse):
    """
    操作成功返回结果类
    """

    code = '1'
    data = []
    message = "success"

    def __init__(self,
                 code=None,
                 data=None,
                 message=None,
                 ):
        super().__init__()
        self.result_dic = dict()
        self.result_dic["message"] = self.message if message is None else message
        self.result_dic["data"] = self.data if data is None else data
        self.result_dic["code"] = self.code if code is None else code


class FailureResponse(BaseResponse):
    """
    操作失败返回结果类
    """

    code = '0'
    data = []
    message = "exception"

    def __init__(self,
                 code=code,
                 data=None,
                 message=None,
                 ):
        super().__init__()
        self.result_dic = dict()
        self.result_dic["message"] = self.message if message is None else message
        self.result_dic["data"] = self.data if data is None else data
        self.result_dic["code"] = self.code if code is None else code
