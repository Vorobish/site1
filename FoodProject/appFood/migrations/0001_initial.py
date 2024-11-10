# Generated by Django 5.1.2 on 2024-11-08 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_created=True)),
                ('name_category', models.CharField(max_length=30)),
                ('image', models.CharField(max_length=200)),
                ('time_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_created=True)),
                ('name_food', models.CharField(max_length=30)),
                ('weight_gr', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=50000)),
                ('ingredients', models.TextField()),
                ('image', models.CharField(max_length=200)),
                ('time_update', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='appFood.category')),
            ],
        ),
    ]