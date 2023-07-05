from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        # customer = request.user.customer
        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        # cartItem = order.get_cart_items
    else:
        # customer = request.user.customer
        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        user_not_login = "show"
        user_login = "hidden"
        # cartItem = order['get_cart_items']

    product = Product.objects.all()
    context = {'products': product, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, 'home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItem = order['get_cart_items']

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)


def payment(request):
    context = {}
    return render(request, 'payment.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password not valid')

    context = {}
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CreateUserForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(Order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    OrderItem.save()

    return JsonResponse('added', safe=False)
# Create your views here.
