# -*- coding: UTF8 -*- #
"""
@filename:city.py
@author:Ajie
@time:2024-07-30
"""
from django.shortcuts import render, redirect

from staffmanage import models
from staffmanage.utils.bootstrap import BootstrapModelForm


def city_list(request):
    """城市列表"""
    queryset = models.City.objects.all()

    return render(request, 'city_list.html', {'city_list': queryset})


class UploadModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def city_add(request):
    """城市添加"""
    if request.method == 'GET':
        form = UploadModelForm()

        return render(request, 'upload_form.html', {'form': form, 'title': '添加城市'})

    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect('/city/list/')

    return render(request, 'upload_form.html', {'form': form, 'title': '添加城市'})
