# Generated by Django 5.1.2 on 2024-11-09 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFood', '0005_alter_orders_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderin',
            name='menu_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderin',
            name='order_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderin',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]