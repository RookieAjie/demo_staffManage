# -*- coding: UTF8 -*- #
"""
@filename:bootstrap.py
@author:Ajie
@time:2024-07-24
"""
from django import forms


class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环ModelForm的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue

            # 字段中有值，则保留原来的属性。若没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label,
                }


class BootstrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
