# Generated by Django 5.0.7 on 2024-07-21 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffmanage', '0002_alter_employee_age_alter_employee_create_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, '一级'), (2, '二级'), (3, '三级'), (4, '四级')], default=1, verbose_name='靓号等级')),
                ('status', models.SmallIntegerField(choices=[(1, '已占用'), (0, '在售')], default=0, verbose_name='靓号状态')),
            ],
        ),
    ]
