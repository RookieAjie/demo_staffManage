# -*- coding: UTF8 -*- #
"""
@filename:admin.py
@author:Ajie
@time:2024-07-24
"""
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from staffmanage import models
from staffmanage.utils.pagination import Pagination
from staffmanage.utils.encrypt import md5


def admin_list(request):
    """管理员列表"""
    # 构造搜索条件
    data_dict = {}
    value = request.GET.get('query', '')
    if value:
        data_dict['username__contains'] = value

    # 根据搜索条件去数据库获取数据
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.HTML(),
        'searchData': value,
    }

    return render(request, 'admin_list.html', context)


from django import forms
from staffmanage.utils.bootstrap import BootstrapModelForm


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致！")
        return confirm_pwd


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 校验当前重置的密码和数据库中的是否相同
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("重置密码不能与旧密码相同！")

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd and pwd is not None:
            raise ValidationError("密码不一致！")
        return confirm_pwd


def admin_add(request):
    """添加管理员"""
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'public.html', {'title': title, 'form': form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'public.html', {'title': title, 'form': form})


def admin_edit(request, admin_id):
    """编辑管理员"""

    row_obj = models.Admin.objects.filter(id=admin_id).first()
    if not row_obj:
        return render(request, 'error.html', {'msg': '数据不存在！'})

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'public.html', {'title': title, 'form': form})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'public.html', {'title': title, 'form': form})


def admin_delete(request, admin_id):
    """删除管理员"""
    models.Admin.objects.filter(id=admin_id).delete()
    return redirect('/admin/list/')


def admin_reset(request, admin_id):
    """重置密码"""
    row_obj = models.Admin.objects.filter(id=admin_id).first()
    if not row_obj:
        return render(request, 'error.html', {'msg': '数据不存在！'})

    title = '重置密码 - {}'.format(row_obj.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'public.html', {'title': title, 'form': form})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'public.html', {'title': title, 'form': form})
