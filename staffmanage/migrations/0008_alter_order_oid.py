# Generated by Django 5.0.7 on 2024-07-29 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffmanage', '0007_order_customer_name_alter_order_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.CharField(max_length=64, unique=True, verbose_name='订单号'),
        ),
    ]