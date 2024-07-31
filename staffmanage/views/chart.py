# -*- coding: UTF8 -*- #
"""
@filename:chart.py
@author:Ajie
@time:2024-07-30
"""
from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """数据统计页面"""

    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图表"""
    legend = ['小A', '小B']

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    series_list = [
        {
            'name': '小A',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 100]
        },
        {
            'name': '小B',
            'type': 'bar',
            'data': [15, 10, 39, 20, 40, 70]
        }
    ]

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'x_axis': x_axis,
            'series_list': series_list
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """构造饼状图数据"""

    db_data_list = [
        {'value': 1048, 'name': 'IT部门'},
        {'value': 735, 'name': '销售部门'},
        {'value': 580, 'name': '基础平台部'},
        {'value': 484, 'name': '企业效率部'},
        {'value': 300, 'name': '后勤部'}
    ]

    result = {
        'status': True,
        'data': db_data_list
    }

    return JsonResponse(result)


def chart_line(request):
    """构造折线图数据"""
    legend = ['湖北', '湖南']

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    series_list = [
        {
            'name': '湖北',
            'type': 'line',
            'stack': 'Total',
            'data': [5, 20, 36, 10, 10, 100]
        },
        {
            'name': '湖南',
            'type': 'line',
            'stack': 'Total',
            'data': [15, 10, 39, 20, 40, 70]
        }
    ]

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'x_axis': x_axis,
            'series_list': series_list
        }
    }

    return JsonResponse(result)
