# encoding: utf-8
"""
@project: djangoModel->api_interrupter_wrapper
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 接口阻断器
@created_time: 2023/7/3 14:53
"""
from django.utils.deprecation import MiddlewareMixin

from utils.custom_tool import parse_request_params


class APIInterrupterMiddleware(MiddlewareMixin):
    """API权限组短期"""

    def process_request(self, request):
        """在视图之前执行"""
        path_info = request.path_info

    def process_view(self, request, view_func, view_args, view_kwargs):
        """在视图之前执行 顺序执行"""
        request_params = parse_request_params(request=request)
        return view_func(request, request_params=request_params)

    def process_response(self, request, response):  # 基于请求响应
        return response
