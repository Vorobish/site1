# Generated by Django 5.1.2 on 2024-11-09 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFood', '0003_orderin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='address',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='comment',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='delivery',
            field=models.CharField(choices=[('avto', 'доставка'), ('self', 'самовывоз')], default='self', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pay_stat',
            field=models.CharField(choices=[('paid', 'оплачен'), ('part', 'аванс'), ('not', 'не оплачен')], default='not', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.IntegerField(choices=[(1, 'создан'), (2, 'принят'), (3, 'отказан'), (4, 'в работе'), (5, 'готов'), (6, 'у курьера'), (7, 'исполнен')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='summa',
            field=models.DecimalField(decimal_places=2, max_digits=500000, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
