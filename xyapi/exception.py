import typing
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as FastapiHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from xyapi.response import ApiResponse


class ApiExceptionHandler:
    def __init__(self, app: FastAPI = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        # todo 自定义异常
        app.add_exception_handler(RequestValidationError, handler=self.request_validation_error_handler)
        app.add_exception_handler(StarletteHTTPException, handler=self.http_exception_handler)
        app.add_exception_handler(FastapiHTTPException, handler=self.http_exception_handler)
        app.add_exception_handler(Exception, handler=self.exception_handler)

    def request_validation_error_handler(self, request: Request, exc: RequestValidationError):
        """ 请求校验错误 """
        return ApiResponse(
            code=HTTPStatus.BAD_REQUEST.value,
            message=HTTPStatus.BAD_REQUEST.phrase,
            data={'detail': exc.errors(), 'body': exc.body}
        )

    def http_exception_handler(self, request: Request, exc: typing.Union[StarletteHTTPException, FastapiHTTPException]):
        """ http异常 """
        return ApiResponse(code=exc.status_code, message=exc.detail)

    def exception_handler(self, request: Request, exc: Exception):
        """ 其他异常 """
        # todo 记录异常日志
        return ApiResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)
