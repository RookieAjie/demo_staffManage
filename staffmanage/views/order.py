# -*- coding: UTF8 -*- #
"""
@filename:order.py
@author:Ajie
@time:2024-07-28
"""
import random
from datetime import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from staffmanage import models
from staffmanage.utils.bootstrap import BootstrapModelForm
from staffmanage.utils.pagination import Pagination


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 将 oid 设置为只读
        self.fields['oid'].widget.attrs['readonly'] = True


def order_list(request):
    """订单列表"""
    # 随机生成oid
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
    form = OrderModelForm(initial={'oid': oid})

    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.HTML()
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):
    """删除订单"""
    delete_id = request.GET.get('delete_id')
    exists = models.Order.objects.filter(id=delete_id).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在！'})

    models.Order.objects.filter(id=delete_id).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    """订单详情"""
    order_id = request.GET.get('id')
    row_obj = models.Order.objects.filter(id=order_id).values('oid', 'title', 'price', 'count', 'status', 'manager',
                                                              'customer_name').first()
    if not row_obj:
        return JsonResponse({'status': False, 'error': '数据不存在！'})

    # 从数据库获取到一个对象：row_obj
    result = {
        'status': True,
        'data': row_obj,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    edit_id = request.GET.get('edit_id')
    row_obj = models.Order.objects.filter(id=edit_id).first()
    if not row_obj:
        return JsonResponse({'status': False, 'tips': '数据不存在！请刷新重试！'})

    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
