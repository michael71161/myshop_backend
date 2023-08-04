from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Category , Order, OrderDetail
from.serializers import ProductSerializer, CategorySerializer , OrderSerializer, OrderDetailSerializer, UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import logout
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
from django.conf import settings
import smtplib


# Create your views here.
#test routes
@api_view(['GET'])
def index(req):
    return Response('hello, this is test route')

@api_view(['GET'])
def mishares(req):
    return Response('Mishares is going straight to the goal!!')


#get all products

@api_view(['GET'])
def getProducts(request, id=0):
    if int(id) > 0:  # return single prod -READ
        prod = Product.objects.filter(_id=id)
    else:  # get All -READ
        prod = Product.objects.all()
    serializer = ProductSerializer(prod, many=True)      
    return Response(serializer.data)




#get all categories

@api_view(['GET'])
def getCategories(request, id=0):
    if int(id) > 0:  # return single prod -READ
        cat = Category.objects.filter(_id=id)
    else:  # get All -READ
        cat = Category.objects.all()
    serializer = CategorySerializer(cat, many=True)      
    return Response(serializer.data)



#upload new product including image field 

class CreateProduct(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=ProductSerializer(data=request.data)
        print(request.data)
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    




# singin, obtain token for the user 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        
        
        
        #convertion of 2 datetime strings , 
        #date time not JSON serializble 
         
        
        
        
        token = super().get_token(user)

        # Add  our custom claims to token payload 
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['email'] = user.email
        token['isAdmin'] = user.is_superuser
        token['userid'] =user.id
        token['lastlogin'] = json.dumps( user.last_login, cls=DjangoJSONEncoder)
        token['datejoined'] =  json.dumps( user.date_joined, cls=DjangoJSONEncoder)
        
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
class TokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


# register/signup
@api_view(['POST'])
def register(request):
    try:
         User.objects.create_user(
            username= request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
            first_name=request.data['first_name']
                                  )
         print( request.data["username"] )
         print( request.data["email"])
         my_email = settings.MY_EMAIL
         email_pass = settings.MY_EMAIL_PASS
         client_email = request.data["email"]
         try:
             with smtplib.SMTP("smtp.gmail.com") as connection:
                 connection.starttls()
                 connection.login(user=my_email,password=email_pass)
                 connection.sendmail(from_addr=my_email,
                        to_addrs={client_email},
                        msg=f"Subject:Welcome to MikesShop!!!\n\n Hello dear {request.data['username']}\n at MikesShop you can find all the smart home gadjets\n Enjoy our site! \n MikesShop team!! ")
         except: print("Email didnt sent")
         return Response("Registration done") 
    except:
         message = {'detail': 'User with this email already exists or other error accured'}
         return Response(message, status=status.HTTP_400_BAD_REQUEST)


# Logout using built in django func
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myLogout(request):
    logout(request)
    return Response("user logged out")




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrder(request):
    order= request.data
    user = request.user
    tempuser = User.objects.get(username=user)
    my_email = settings.MY_EMAIL
    email_pass = settings.MY_EMAIL_PASS
    client_email = tempuser.email
    print(user)
    print(client_email)
    print(my_email)
    
    order_total=0
    for x in order:
        prod_total= x["total"]
        order_total= order_total + int(prod_total)
    # total_order= request.data[""]
    new_order_id= Order.objects.create(user_id=user, total=order_total)
    print(order)
    for x in order:
        print(x)
        prod_id=Product.objects.get(_id=x["_id"])
        prod_amount= x["amount"]
        prod_total= x["total"]
        # category_id=Category.objects.get(_id=x["category_id"])
        OrderDetail.objects.create(order_id=new_order_id,product_id=prod_id,amount= prod_amount, total=prod_total)
    try:
     with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email,password=email_pass)
        connection.sendmail(from_addr=my_email,
                        to_addrs={client_email},
                        msg=f"Subject:Your order at MikesShop has been confirmed!\n\n Hello dear {user}\n we received your order!!\n Total amount: {order_total} NIS \n Thank you from MikeShop team ")
    except: print("Email didnt sent")
    return Response("Order created")




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userOrders(request):
    user = request.user
    oldOrders= user.order_set.all()
    serializer = OrderSerializer(oldOrders, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderDetails(request, id=0):
    order_id = Order.objects.get(_id=id)
    orderDetails=OrderDetail.objects.filter(order_id=order_id)
    serializer = OrderDetailSerializer(orderDetails, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updUser(request,id):
    try:
        temp = User.objects.get(id=id)
        temp.username = request.data['newUsername']
        temp.email = request.data["newEmail"]
        temp.first_name = request.data['newFirst_name']
        temp.save()
        print(temp.username, temp.first_name)
        return Response("user details has been updated")
    except:
        return  Response("Error, check details or try again later")



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    return Response(serializer.data)

        





