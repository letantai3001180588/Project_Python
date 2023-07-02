from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def home(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request,'home.html',context)
def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_oncreate(customer = customer)
    #     items = order.orderitem_set_all()
    # else:
    #     items = []
    context = {}
    return render(request,'cart.html',context)
def payment(request):
    context = {}
    return render(request,'payment.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password not valid')

    context = {}
    return render(request,'login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def register(request):
    form = CreateUserForm()
    context = {'form':form}
    return render(request,'register.html',context)

# Create your views here.
