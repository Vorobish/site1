# Generated by Django 5.1.2 on 2024-11-08 21:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFood', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_created=True)),
                ('summa', models.DecimalField(decimal_places=2, max_digits=500000)),
                ('delivery', models.CharField(choices=[('avto', 'доставка'), ('self', 'самовывоз')], default='self', max_length=4)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField(max_length=200)),
                ('pay_stat', models.CharField(choices=[('paid', 'оплачен'), ('part', 'аванс'), ('not', 'не оплачен')], default='not', max_length=4)),
                ('status', models.IntegerField(choices=[(1, 'создан'), (2, 'принят'), (3, 'отказан'), (4, 'в работе'), (5, 'готов'), (6, 'у курьера'), (7, 'исполнен')], default=1)),
                ('comment', models.TextField(max_length=500)),
                ('time_update', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]