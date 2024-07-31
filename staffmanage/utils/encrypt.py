# -*- coding: UTF8 -*- #
"""
@filename:encrypt.py
@author:Ajie
@time:2024-07-25
"""
from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
