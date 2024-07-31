"""
URL configuration for demo_staffManage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from staffmanage.views import department, user, prettyNumber, admin, account, task, order, chart, upload, city

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 启用 media 目录
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 设置启动时默认页面
    path('', account.login),

    # 部门管理
    path('depart/list/', department.depart_list),
    path('depart/add/', department.depart_add),
    path('depart/delete/', department.depart_delete),
    path('depart/<int:depart_id>/edit/', department.depart_edit),
    path('depart/upload/', department.depart_upload),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/modelform/add/', user.user_modelform_add),
    path('user/<int:user_id>/edit/', user.user_edit),
    path('user/<int:user_id>/delete/', user.user_delete),

    # 靓号管理
    path('prettynum/list/', prettyNumber.prettynum_list),
    path('prettynum/add/', prettyNumber.prettynum_add),
    path('prettynum/<int:pretty_id>/edit/', prettyNumber.prettynum_edit),
    path('prettynum/<int:pretty_id>/delete/', prettyNumber.prettynum_delete),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:admin_id>/edit/', admin.admin_edit),
    path('admin/<int:admin_id>/delete/', admin.admin_delete),
    path('admin/<int:admin_id>/reset/', admin.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/captcha/', account.image_captcha),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),

    # 上传文件
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    path('upload/model/form/', upload.upload_model_form),

    # 城市列表
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),

]
