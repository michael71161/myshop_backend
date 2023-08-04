"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    
    path('', views.index),
    path('misha/', views.mishares),
    path('products/', views.getProducts),
    path('products/<id>', views.getProducts),
    path('category/', views.getCategories),
    path('category/<id>', views.getCategories),
    path('upload/',views.CreateProduct.as_view()),
    
    
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register),
    path('logout/',views.myLogout),
    path('addorder/', views.addOrder),
    path('userorders/', views.userOrders),
    path('orderdetails/<id>',views.orderDetails),
    path('upduser/<id>', views.updUser),
    path('getusers/', views.getUsers)
]
