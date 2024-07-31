# -*- coding: UTF8 -*- #
"""
@filename:upload.py
@author:Ajie
@time:2024-07-30

备注：这是个测试上传文件的页面
"""
import os

from django import forms
from django.shortcuts import render
from django.http import HttpResponse

from staffmanage.utils.bootstrap import BootStrapForm, BootstrapModelForm
from staffmanage import models


def upload_list(request):
    """上传文件"""
    if request.method == 'GET':
        return render(request, 'upload_list.html')

    file_obj = request.FILES['file']
    with open(file_obj.name, mode='wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    return HttpResponse('...')


class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(max_length=128, label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    if request.method == 'GET':
        form = UploadForm()
        context = {
            'form': form,
            'title': 'Form上传文件',
        }
        return render(request, 'upload_form.html', context)

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # {'name': '张三1', 'age': 12, 'img': <InMemoryUploadedFile: sightseeing1.png (image/png)>}
        # print(form.cleaned_data)

        # 1 读取图片内容，写到文件夹中并获取文件的路径
        img_obj = form.cleaned_data.get('img')

        # img_path = 'staffmanage/fileStorage/avatar/{}'.format(img_obj.name) 为避免不同系统分隔符问题：
        db_img_path = os.path.join('media', 'avatar', img_obj.name)  # 注意：会有重名问题，modelform可避免

        with open(db_img_path, mode='wb') as f:
            for chunk in img_obj.chunks():
                f.write(chunk)

        # 2 将图片路径写入到数据库中
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_img_path,
        )

        return HttpResponse('ok')

    context = {
        'form': form,
        'title': 'Form上传文件',
    }
    return render(request, 'upload_form.html', context)


class UploadModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def upload_model_form(request):
    """上传文件和数据(modelForm)"""

    if request.method == 'GET':
        form = UploadModelForm()

        return render(request, 'upload_form.html', {'form': form, 'title': 'ModelForm上传文件'})

    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        return HttpResponse('ok')

    return render(request, 'upload_form.html', {'form': form, 'title': 'ModelForm上传文件'})