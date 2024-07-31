from django.db import models


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=32, verbose_name='部门名')

    def __str__(self):
        return self.title


class Employee(models.Model):
    """ 员工表 """
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=32, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.CharField(max_length=16, verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='账户余额')
    # create_time = models.DateTimeField(verbose_name='入职日期')
    create_time = models.DateField(verbose_name='入职日期')

    # 若部门表删除了该怎么办？此时depart是外键，有两种解决方案：
    # 1 级联删除
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE, verbose_name='所属部门')

    # 2 将此列对应的值置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    # 性别的设置
    # 不推荐使用字典，因为Django的choices参数是专门设计来与二元元组列表一起使用
    # 在Django模型中，choices字段需要使用一个包含元组的列表，而不是包含字典的列表。
    # 因为Django期望的格式是一个元组列表，其中每个元组的第一个元素是存储在数据库中的值，第二个元素是用于显示的值。
    gender_choices = [
        (1, '男'),
        (2, '女')
    ]
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    def __str__(self):
        return self.name


class PrettyNumber(models.Model):
    """靓号表"""
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    # 若要允许为空：null=True, blank=True
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    level = models.SmallIntegerField(choices=level_choices, verbose_name='靓号等级', default=1)

    status_choices = (
        (1, '已占用'),
        (0, '在售'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='靓号状态', default=0)


class Task(models.Model):
    """任务"""

    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '普通')
    )
    level = models.SmallIntegerField(choices=level_choices, default=3, verbose_name='任务级别')
    title = models.CharField(max_length=64, verbose_name='任务标题')
    manager = models.ForeignKey(to='Admin', on_delete=models.CASCADE, verbose_name='任务负责人')
    detail = models.TextField(verbose_name='任务详情')


class Order(models.Model):
    """订单"""
    oid = models.CharField(max_length=64, verbose_name='订单号', null=False, unique=True)
    title = models.CharField(max_length=32, verbose_name='产品名称')
    price = models.IntegerField(verbose_name='价格')
    count = models.IntegerField(verbose_name='订购数量', default=1)

    status_choices = (
        (0, '待支付'),
        (1, '已支付'),
    )
    status = models.SmallIntegerField(verbose_name='订单状态', choices=status_choices, default=0)
    customer_name = models.CharField(verbose_name='雇主姓名', max_length=32, default='匿名用户')

    manager = models.ForeignKey(to='Employee', verbose_name='订单负责人', on_delete=models.CASCADE)


class Boss(models.Model):
    """老板"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=128)


class City(models.Model):
    """城市"""
    name = models.CharField(verbose_name='名称', max_length=32)
    population = models.IntegerField(verbose_name='人口')

    # 本质上数据也是CharField，但是存储的是文件路径
    img = models.FileField(verbose_name='Logo', max_length=128, upload_to='city/')
