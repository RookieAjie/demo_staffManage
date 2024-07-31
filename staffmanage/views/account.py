# -*- coding: UTF8 -*- #
"""
@filename:account.py
@author:Ajie
@time:2024-07-25
"""
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from staffmanage import models
from staffmanage.utils.encrypt import md5
from staffmanage.utils.captcha import check_code


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'id': 'username',
                                      'placeholder': '请输入用户名'}),
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'id': 'password',
                                          'placeholder': '请输入密码'},
                                   render_value=True),
        required=True,
    )
    captcha = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'id': 'captcha',
                                      'placeholder': '请输入验证码'}),
        required=True,
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


def login(request):
    """登录"""

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        # 验证码的校验
        user_captcha = form.cleaned_data.pop('captcha')
        captcha = request.session.get('image_captcha', '')
        if captcha.upper() != user_captcha.upper():
            form.add_error('captcha', '验证码错误！')
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取对象。
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error('password', '用户名或密码错误！')
            return render(request, 'login.html', {'form': form})

        # 若验证通过：
        # 网站生成随机字符串，写入用户浏览器的cookie中。再写入session中
        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        # session保存7天
        request.session.set_expiry(60 * 60 * 25 * 7)

        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def image_captcha(request):
    """生成图片验证码"""

    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # print(code_string)

    # 写入到自己的session中，以便于后续的校验
    request.session['image_captcha'] = code_string
    # 给此session设置超时时间
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, format='png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')
