# -*- coding: UTF8 -*- #
"""
@filename:user.py
@author:Ajie
@time:2024-07-24
"""
from django.shortcuts import render, redirect
from staffmanage import models

from staffmanage.utils.pagination import Pagination
from staffmanage.utils.form import UserModelForm


def user_list(request):
    """用户列表"""

    # 获取所有的用户列表【obj，ovj，obj，】
    queryset = models.Employee.objects.all()
    """
        # 用python语法获取数据
        for employee in queryset:
            print(employee.id, employee.name, employee.account, employee.create_time.strftime('%Y-%m-%d'),
                  employee.get_gender_display(), employee.depart.title)    
        """

    # 使用封装好的类进行分页
    page_obj = Pagination(request, queryset)

    context = {
        'employees': page_obj.page_queryset,
        'page_string': page_obj.HTML(),
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户"""

    if request.method == "GET":
        context = {
            'gender_choices': models.Employee.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    """
    使用try except来预防空值
    try:
        username = request.POST.get('userName')
        user_pwd = request.POST.get('userPwd')
        user_age = request.POST.get('userAge')
        user_account = request.POST.get('userAccount')
        user_ctime = request.POST.get('userCtime')
        user_gender = request.POST.get('userGender')
        user_depart = request.POST.get('userDepart')

        # 判断是否有空值
        if not all([username, user_pwd, user_age, user_account, user_ctime, user_gender, user_depart]):
            return redirect('/user/add/')

    except Exception as e:
        # 处理可能的其他异常
        print(f"An error occurred: {e}")
    """

    # 另一种预防空值的办法：request.POST.get()方法会返回空字符串（如果字段未填写）
    username = request.POST.get('userName')
    user_pwd = request.POST.get('userPwd')
    user_age = request.POST.get('userAge')
    user_account = request.POST.get('userAccount')
    user_ctime = request.POST.get('userCtime')
    user_gender = request.POST.get('userGender')
    user_depart = request.POST.get('userDepart')

    if '' in [username, user_pwd, user_age, user_account, user_ctime, user_gender, user_depart]:
        return redirect('/user/add/')

    # 将数据添加至数据库
    models.Employee.objects.create(name=username, password=user_pwd, age=user_age, account=user_account,
                                   create_time=user_ctime, gender=user_gender, depart_id=user_depart)

    # 返回用户列表
    return redirect('/user/list')


def user_modelform_add(request):
    """添加用户（基于ModelForm）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_modelform_add.html', {"form": form})

    # 用户 POST 提交数据，进行校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')

    # print(form.errors)
    return render(request, 'user_modelform_add.html', {"form": form})


def user_edit(request, user_id):
    """编辑用户信息"""

    # 根据ID去数据库获取要编辑的那一行的数据（对象）
    row_obj = models.Employee.objects.filter(id=user_id).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, user_id):
    models.Employee.objects.filter(id=user_id).delete()
    return redirect('/user/list/')
