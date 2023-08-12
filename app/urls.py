from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart', views.cart,name='cart'),
    path('payment', views.payment,name='payment'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.register, name='register'),
    path('search', views.search, name='search'),
    path('update_item/', views.updateItem, name='update_item/'),
    path('delete_item/<str:id>/', views.deleteItem, name='delete_item/'),
    path('detail/<str:id>/', views.detail, name='detail/'),
    path('changePassword/', views.changePasswod, name='changePassword/'),
    path('profile/', views.update_profile, name='profile/'),
    path('historyOrder/', views.history, name='historyOrder/'),
    path('email/', views.email, name='email/'),
]
