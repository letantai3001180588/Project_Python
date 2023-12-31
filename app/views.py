from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItem = order['get_cart_items']

    product = Product.objects.all()
    context = {'products': product, 'cart': cartItem}
    return render(request, 'home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItem = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart': cartItem}
    return render(request, 'cart.html', context)


def payment(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    if request.method == 'POST':
        customer = request.user
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        ship, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        ship.address = address
        ship.phone = phone
        order.save()
        ship.save()
        items = order.orderitem_set.all()
        context = {'items': items, 'order': order, 'customer': customer, 'phone': phone, 'address': address}
        subject = 'Bạn đã đặt hàng thành công từ Laptops Shop'
        from_email = 'taile07032000@gmail.com'
        user = User.objects.get(username=customer)
        user_email = user.email
        recipient_list = [user_email]
        html_message = render_to_string('email.html', context)
        plain_message = strip_tags(html_message)
        sent = send_mail(subject=subject, message=plain_message,   from_email=from_email, recipient_list=recipient_list, html_message=html_message)
        if sent != 0:
            # return render(request, 'email.html', context)
            return redirect('home')
            # return HttpResponse('Gửi email thành công.')
        else:
            return HttpResponse('Không thể gửi được email đến!')


    context2 = {'order': order, 'items': items}
    return render(request, 'payment.html', context2)


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
            messages.info(request, 'Username or password not valid')

    context = {}
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def updateItem(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        quantity = data['quantity']
        customer = request.user
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add' and product.quantity > quantity:
            orderItem.quantity += 1
            orderItem.save()
            return JsonResponse('Thêm 1 số lượng sản phẩm thành công!', safe=False)
        elif action == 'remove' and quantity > 1:
            orderItem.quantity -= 1
            orderItem.save()
            return JsonResponse('Giảm 1 số lượng sản phẩm thành công!', safe=False)

        else:
            return JsonResponse('Số lượng sản phẩm vượt giới hạn!', safe=False)
        return JsonResponse('Lỗi', safe=False)


def search(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    if request.method == "POST":
        search = request.POST['searched']
        key = Product.objects.filter(name__contains=search)
    context = {'search': search, 'key': key, 'cart': cartItem}
    return render(request, 'search.html', context)


def deleteItem(request, id):
    productDelete = get_object_or_404(OrderItem, id=id)
    productDelete.delete()
    return redirect('cart')


def detail(request, id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cartItem = []
    product = Product.objects.filter(id=id)
    context = {'product': product, 'cart': cartItem}
    return render(request, 'detail.html', context)


@login_required()
def changePasswod(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.info(request, 'password is not valid')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'changePassword.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.info(request, 'Can not update user')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def history(request):
    customer = request.user
    order = Order.objects.filter(customer=request.user, complete=True)
    # orderItem, created = OrderItem.objects.get_or_create(order=order.transaction_id)
    # orderItem = OrderItem.objects.get(order=order)
    # items = order.orderitem_set.all()
    context = {'order': order}
    return render(request, 'historyOrder.html', context)


def email(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    context = {}
    return render(request, 'email.html', context)
