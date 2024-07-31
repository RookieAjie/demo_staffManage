# -*- coding: UTF8 -*- #
"""
@filename:prettyNumber.py
@author:Ajie
@time:2024-07-24
"""
from django.shortcuts import render, redirect
from staffmanage import models

from staffmanage.utils.pagination import Pagination
from staffmanage.utils.form import PrettyModelForm, PrettyEditModelForm


def prettynum_list(request):
    """靓号列表"""
    data_dict = {}
    value = request.GET.get('query', '')
    if value:
        data_dict['mobile__contains'] = value

    # 数据分页
    # select sth from 表 order by level desc;
    queryset = models.PrettyNumber.objects.filter(**data_dict).order_by('-level')

    page_obj = Pagination(request, queryset)  # 实例化分页类

    context = {'searchData': value,
               'prettyNums': page_obj.page_queryset,  # 分完页的数据
               'page_string': page_obj.HTML()  # 页码
               }

    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    """添加靓号"""

    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'prettynum_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')

    return render(request, 'prettynum_add.html', {"form": form})


def prettynum_edit(request, pretty_id):
    """编辑靓号"""

    row_obj = models.PrettyNumber.objects.filter(id=pretty_id).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, 'prettynum_edit.html', {'form': form})

    form = PrettyEditModelForm(instance=row_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')

    return render(request, 'prettynum_edit.html', {"form": form})


def prettynum_delete(request, pretty_id):
    models.PrettyNumber.objects.filter(id=pretty_id).delete()
    return redirect('/prettynum/list/')
