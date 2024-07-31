# -*- coding: UTF8 -*- #
"""
@filename:task.py
@author:Ajie
@time:2024-07-28
"""
import json

from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from staffmanage import models
from staffmanage.utils.bootstrap import BootstrapModelForm
from staffmanage.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            'detail': forms.TextInput
        }


def task_list(request):
    """任务管理"""
    # 去数据库获取所有的任务信息
    queryset = models.Task.objects.all().order_by('level')
    page_object = Pagination(request, queryset)

    form = TaskModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.HTML()  # 生成页码
    }

    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    print(request.POST)

    data_dict = {'status': True, 'data': [11, 22, 33, 44]}
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)


@csrf_exempt
def task_add(request):
    """添加任务"""
    # QueryDict: {'level': ['3'], 'title': ['fsdf'], 'manager': ['7'], 'detail': ['sdfsd']}
    print(request.POST)

    # 1 用户发来的数据进行校验(ModelForm)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict))
