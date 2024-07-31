# -*- coding: UTF8 -*- #
"""
@filename:auth.py
@author:Ajie
@time:2024-07-25
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):
    """用户认证中间件"""

    def process_request(self, request):
        # 首先排除不需要验证就能访问的页面（登录页面）
        # request.path_info 获取用户当前访问的url
        if request.path_info in ['/login/', '/image/captcha/']:
            return

        # 1 读取当前访问用户的session信息。若能读到，说明用户已登录。
        info_dict = request.session.get('info')
        if info_dict:
            return

        return redirect('/login/')