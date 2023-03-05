import decimal
import json
import datetime
from typing import Any
from fastapi.responses import JSONResponse


class CustomJsonEncoder(json.JSONEncoder):
    """ 自定义Json编码器 """

    def default(self, o: Any) -> Any:
        # dict
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # datetime
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        # date
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        # decimal
        if isinstance(o, decimal.Decimal):
            return float(o)
        # bytes
        if isinstance(o, bytes):
            return str(o, encoding='utf-8')
        # object
        if hasattr(o, '__dict__'):
            return o.__dict__
        # default
        return super().default(o)


class ApiResponse(JSONResponse):
    """ 接口响应对象 """
    http_status_code: int = 200
    code: int = None
    message: str = None
    data: Any = None

    def __init__(self, data=None, code=None, message=None, http_status_code=None, **kwargs) -> None:
        if data is not None:
            self.data = data
        if code:
            self.code = code
        if message:
            self.message = message
        if http_status_code:
            self.http_status_code = http_status_code

        # 响应体
        body = dict(
            code=self.code,
            message=self.message,
            data=self.data
        )

        # 可选参数
        if kwargs:
            # 合并到响应体
            body = {**body, **kwargs}
            # 排除非标准的可选参数
            includes = ['content', 'status_code', 'headers', 'media_type', 'background']
            for key in kwargs.keys():
                if key not in includes:
                    kwargs.pop(key)

        # 调用父类初始化方法
        super().__init__(status_code=self.http_status_code, content=body, **kwargs)

    def render(self, content: Any) -> bytes:
        """ 框架调用，需要特殊处理的地方可以在这里统一处理 """
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            cls=CustomJsonEncoder
        ).encode("utf-8")


class Ok(ApiResponse):
    code = 200
    message = 'ok'


class Error(ApiResponse):
    code = 500
    message = 'error'
