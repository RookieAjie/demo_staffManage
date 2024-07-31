from django.utils.safestring import mark_safe
import copy

# -*- coding: UTF8 -*- #
"""
@filename:pagination.py
@author:Ajie
@time:2024-07-23
"""

"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            'queryset': page_object.page_queryset,  # 分完页的数据
            'page_string': page_object.HTML()       # 生成页码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中：

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = self.start + page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()

        # 总页码
        total_page, div = divmod(total_count, page_size)
        if div:
            total_page += 1

        self.total_page = total_page
        self.plus = plus

    def HTML(self):
        # 计算出显示当前页的前5页，后5页
        if self.total_page <= 2 * self.plus + 1:
            # 数据库中数据较少，未达到 11 页
            start_page = 1
            end_page = self.total_page
        else:
            # 数据库中数据较多，超过了 11 页
            # 当前page < 5 时：（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前page > 5 时：（大极值）
                if self.page + self.plus > self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            # 第一页的上一页不能被点击（或者强制写为1）
            self.query_dict.setlist(self.page_param, [1])
            prev_page = '<li style="pointer-events: none"><a href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev_page)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                element = '<li  class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                element = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(element)

        # 下一页
        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            # 最后一页的下一页不能被点击（或者强制写为total_page）
            self.query_dict.setlist(self.page_param, [self.total_page])
            next_page = '<li style="pointer-events: none"><a href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(next_page)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 页码跳转框
        search_string = """
                <li>
                    <form action="#" style="float: left;margin-left: 1px" method="get">
                        <label for="page">
                            <input type="text" name="page" id="page"
                                   style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0"
                                   class="form-control" placeholder="页码...">
                        <button style="border-radius: 0" class="btn btn-default">跳转</button>
                        </label>    
                    </form>
                </li>
            """

        page_str_list.append(search_string)

        # 将其转为字符串
        page_string = mark_safe("".join(page_str_list))
        return page_string
