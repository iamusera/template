import json

from flask import request
from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    code = '0'
    msg = 'internal error'
    data = ''

    # 自定义需要返回的信息，在初始化完成并交给父类
    def __init__(self, msg=None, code=None, data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(ApiException, self).__init__(msg, None)

    def get_body(self, environ=None, scop=None):
        body = dict(
            code=self.code,
            msg=self.msg,
            # request=request.method + ' ' + self.get_url_no_parm(),
            data=self.data
        )
        # sort_keys 取消排序规则，ensure_ascii 中文显示
        text = json.dumps(body, sort_keys=False, ensure_ascii=False)
        return text

    def get_headers(self, environ=None, scop=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_parm():
        full_path = str(request.path)
        return full_path
