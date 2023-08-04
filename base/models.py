from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    _id=models.AutoField(primary_key=True,editable=False)
    desc =models.CharField(max_length=50,null=False,blank=False)
    
    def __str__(self):
     	return f'Category id: {self._id}, Category desc: {self.desc}'  #what we will see in the admin panel 


class Product(models.Model):
    _id=models.AutoField(primary_key=True,editable=False)
    category_id= models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    prod_name = models.CharField(max_length=50,null=True,blank=True)
    desc = models.CharField(max_length=150,null=True,blank=True)
    price = models.DecimalField(max_digits=4,decimal_places=0,default=0)
    image = models.ImageField(upload_to='Posted_Images',null=True,blank=True,default='/placeholder.png')
    createdTime=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
     	return f'ID: {self._id}, mame: {self.prod_name}, Price: {self.price}, Category desc: {self.category_id.desc}, CreatedTime: {self.createdTime}'
  



class Order(models.Model):
    _id=models.AutoField(primary_key=True,editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False,blank=False)
    createdTime=models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0, null=True,blank=True)
    


    def __str__(self):
     	return f'ID: {self._id}, User id: {self.user_id.id}, Username: {self.user_id.username}, CreatedTime: {self.createdTime}, Total: {self.total}'  



class OrderDetail(models.Model):
    _id=models.AutoField(primary_key=True,editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False,blank=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,blank=False)
    amount= models.IntegerField(default=1, null=True,blank=True)
    total = models.IntegerField(default=1, null=True,blank=True)

    def __str__(self):
     	return f'ID: {self._id}, Order id: {self.order_id._id}, User id: {self.order_id.user_id.id}, Username: {self.order_id.user_id.username}, Product id: {self.product_id._id}, Product desc: {self.product_id.desc}, Product amount: {self.amount}, Total: {self.total}'