from django.contrib import admin
from .models import Product, Category, Order, OrderDetail
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderDetail)
