from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CustomUserCreationForm, LoginForm
from .models import *


def base(request):
    '''
        Главная страница
    '''
    title = 'Главная страница'
    content = 'Для выбора товаров перейдите в Меню'
    if request.user.is_authenticated:
        user = request.user
    else:
        user = 'гость'
    context = {
        'title': title,
        'user': user,
        'content': content,
    }
    return render(request, 'base.html', context)


class LoginUser(LoginView):
    '''
        Класс авторизации
    '''
    form_class = LoginForm
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    '''
        Функция выхода из ЛК
    '''
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    '''
        Регистрация пользователя
    '''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if not form.email_clean():
                form.save()
                messages.success(request, 'Успешная регистрация')
            else:
                messages.success(request, 'Данный Email уже существует')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
        'title': 'Регистрация',
    }
    return render(request, 'register.html', context)


k = 3  # кол-во объектов на странице


def menu(request):
    '''
        Страница Меню - выбор товаров
    '''
    title = 'Меню'
    global k
    global basket_list
    if request.method == 'POST':
        if 'pag' in request.POST:
            k = request.POST.get('k')
        if 'add' in request.POST:
            menu_id = int(request.POST.get('menu.id'))
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.POST:
            menu_id = int(request.POST.get('menu.id'))
            if menu_id in basket_list:
                if basket_list[menu_id] > 1:
                    basket_list[menu_id] -= 1
                elif basket_list[menu_id] == 1:
                    basket_list.pop(menu_id)

    menus = Menu.objects.all().order_by('id')
    paginator = Paginator(menus, k)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'page_obj': page_obj,
        'k': k,
        'basket_list': basket_list,
    }
    return render(request, 'menu.html', context)


basket_list = {}


def basket(request):
    '''
        Страница корзина - оформление заказа
    '''
    global basket_list
    list_info = {}
    res = 0
    messages = ''
    for i in basket_list:
        name = Menu.objects.filter(id=i).values_list('name_food', flat=True)[0]
        price = Menu.objects.filter(id=i).values_list('price', flat=True)[0]
        amount = basket_list[i]
        list_info.update({i: f"{name}, количество = {amount}, сумма: {price} руб. * {amount} = {price * amount} руб."})
        res += price * amount
    if request.method == 'POST':
        if 'add' in request.POST:
            menu_id = int(request.POST.get('key'))
            if menu_id in basket_list:
                basket_list[menu_id] += 1
            else:
                basket_list.update({menu_id: 1})
        if 'del' in request.POST:
            menu_id = int(request.POST.get('key'))
            if menu_id in basket_list:
                if basket_list[menu_id] > 1:
                    basket_list[menu_id] -= 1
                elif basket_list[menu_id] == 1:
                    basket_list.pop(menu_id)
        if 'order' in request.POST:
            if request.user.is_authenticated:
                user_id = int(request.POST.get('user_id'))
                deli = request.POST.get('deli') == 'on'
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                comment = request.POST.get('comment')
                delivery = 'self'
                if deli:
                    res += 200
                    delivery = 'avto'
                Orders.objects.create(user_id=user_id,
                                      summa=res,
                                      delivery=delivery,
                                      phone=phone,
                                      address=address,
                                      comment=comment)
                number = int(Orders.objects.latest('id').id)
                for i in basket_list:
                    price = Menu.objects.filter(id=i).values_list('price', flat=True)[0]
                    count = int(basket_list[i])
                    summa = price * count
                    OrderIn.objects.create(order_id=number,
                                           menu_id=i,
                                           count=count,
                                           summa=summa)
                basket_list.clear()
                list_info.clear()
                messages = f'Заказ создан, номер {number}'
            else:
                messages = 'Для оформления заказа нужно авторизоваться'
    title = 'Корзина'
    context = {
        'title': title,
        'list_info': list_info,
        'res': res,
        'messages': messages,
    }
    return render(request, 'basket.html', context)


order_id = None


def orders(request):
    '''
        Страница с заказами пользователя
    '''
    global order_id
    orderss = Orders.objects.filter(user_id=request.user.id).order_by('-id')
    if request.method == 'POST':
        if 'info' in request.POST:
            order_id = int(request.POST.get('order_id'))
    title = 'Заказы'
    context = {
        'title': title,
        'orderss': orderss,
    }
    return render(request, 'orders.html', context)


def order(request):
    '''
        Страница с данными о конкретном заказе пользователя
    '''
    order_id = request.GET.get('order_id')
    summa = Orders.objects.filter(id=order_id).values_list('summa', flat=True)[0]
    delivery = Orders.objects.filter(id=order_id).values_list('delivery', flat=True)[0]
    deli_info = ''
    if delivery == 'avto':
        deli_info = 'с доставкой (200 руб.)'
    else:
        deli_info = 'самовывоз'
    pay_stat = Orders.objects.filter(id=order_id).values_list('pay_stat', flat=True)[0]
    pay_info = ''
    if pay_stat == 'paid':
        pay_info = 'заказ оплачен'
    elif pay_stat == 'part':
        pay_info = 'внесен аванс'
    else:
        pay_info = 'не оплачен'
    phone = Orders.objects.filter(id=order_id).values_list('phone', flat=True)[0]
    address = Orders.objects.filter(id=order_id).values_list('address', flat=True)[0]
    status = Orders.objects.filter(id=order_id).values_list('status', flat=True)[0]
    stat_info = ''
    if status == 1:
        stat_info = 'создан'
    elif status == 2:
        stat_info = 'принят'
    elif status == 3:
        stat_info = 'отказан'
    elif status == 4:
        stat_info = 'в работе'
    elif status == 5:
        stat_info = 'готов'
    elif status == 6:
        stat_info = 'у курьера'
    else:
        stat_info = 'исполнен'
    comment = Orders.objects.filter(id=order_id).values_list('comment', flat=True)[0]
    time_create = Orders.objects.filter(id=order_id).values_list('time_create', flat=True)[0]
    detail = OrderIn.objects.filter(order_id=order_id).order_by('menu_id')
    list_detail = []
    for i in detail:
        menu_id = OrderIn.objects.filter(id=i.id).values_list('menu_id', flat=True)[0]
        count = OrderIn.objects.filter(id=i.id).values_list('count', flat=True)[0]
        name = Menu.objects.filter(id=menu_id).values_list('name_food', flat=True)[0]
        price = Menu.objects.filter(id=menu_id).values_list('price', flat=True)[0]
        list_detail.append(f"{name}, количество = {count}, сумма: {price} руб. * {count} = {price * count} руб.")
    title = 'Детали заказа'
    context = {
        'title': title,
        'order_id': order_id,
        'summa': summa,
        'deli_info': deli_info,
        'phone': phone,
        'address': address,
        'pay_info': pay_info,
        'stat_info': stat_info,
        'comment': comment,
        'time_create': time_create,
        'list_detail': list_detail,
    }
    return render(request, 'order.html', context)
