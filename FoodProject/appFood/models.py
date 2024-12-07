from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Menu(models.Model):
    '''
        Меню - товар в меню
    '''
    name_food = models.CharField(max_length=30)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    weight_gr = models.IntegerField()
    price = models.DecimalField(max_digits=50000, decimal_places=2)
    ingredients = models.TextField()
    image = models.CharField(max_length=200)
    time_create = models.DateTimeField(auto_created=True)
    time_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_food


class Category(models.Model):
    '''
        Категория товара из меню
    '''
    name_category = models.CharField(max_length=30)
    image = models.CharField(max_length=200)
    time_create = models.DateTimeField(auto_created=True)
    time_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_category


class Orders(models.Model):
    '''
        Заказ
    '''
    Type_delivery = [
        ('avto', 'доставка'),
        ('self', 'самовывоз'),
    ]

    Type_payment = [
        ('paid', 'оплачен'),
        ('part', 'аванс'),
        ('not', 'не оплачен'),
    ]

    Type_status = [
        (1, 'создан'),
        (2, 'принят'),
        (3, 'отказан'),
        (4, 'в работе'),
        (5, 'готов'),
        (6, 'у курьера'),
        (7, 'исполнен'),
    ]

    user_id = models.IntegerField()
    summa = models.DecimalField(max_digits=500000, decimal_places=2, null=True)
    delivery = models.CharField(max_length=4, choices=Type_delivery, default='self', null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.TextField(max_length=200, null=True)
    pay_stat = models.CharField(max_length=4, choices=Type_payment, default='not', null=True)
    status = models.IntegerField(choices=Type_status, default=1, null=True)
    comment = models.TextField(max_length=500, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now_add=True)


class OrderIn(models.Model):
    '''
        Состав заказа
    '''
    order_id = models.IntegerField(null=True)
    menu_id = models.IntegerField(null=True)
    count = models.IntegerField(null=True)
    summa = models.DecimalField(max_digits=500000, decimal_places=2, null=True)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now_add=True, null=True)

# python manage.py makemigrations
# python manage.py migrate
