from rest_framework.serializers import ModelSerializer
from . models import Product, Category , Order, OrderDetail
from django.contrib.auth.models import User
#from rest_framework import serializers

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
        
class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        
        
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

