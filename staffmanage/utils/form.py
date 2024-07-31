# -*- coding: UTF8 -*- #
"""
@filename:form.py
@author:Ajie
@time:2024-07-24
"""
from staffmanage import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from staffmanage.utils.bootstrap import BootstrapModelForm


class UserModelForm(BootstrapModelForm):
    name = forms.CharField(min_length=2, label='姓名')

    class Meta:
        model = models.Employee
        # fields = '__all__'
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }


class PrettyModelForm(BootstrapModelForm):
    class Meta:
        model = models.PrettyNumber
        fields = '__all__'

    # 验证手机号合法性。方式一：
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误")]
    )

    # 验证手机号合法性：
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        exist = models.PrettyNumber.objects.filter(mobile=txt_mobile).exists()

        if exist:
            raise ValidationError("手机号已经存在！")

        # 若验证通过，则返回用户输入的值
        return txt_mobile


class PrettyEditModelForm(BootstrapModelForm):
    mobile = forms.CharField(disabled=True)

    class Meta:
        model = models.PrettyNumber
        fields = ['mobile', 'price', 'level', 'status']

    # # 验证手机号合法性：(已经设置不可编辑)
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data['mobile']
    #
    #     exist = models.PrettyNumber.objects.filter(mobile=txt_mobile).exists()
    #
    #     if exist:
    #         raise ValidationError("手机号已经存在！")
    #
    #     # 若验证通过，则返回用户输入的值
    #     return txt_mobile
