from django.db import models
from django.contrib.auth.models import User

# Create your models here.

EMP_POSITION = (
    (1, "Manager"),
    (2, "Assistant Manager"),
    (3, "Cashier"),
    (4, "Barista"),
    (5, "Baker"),
    (6, "Server"),
    (7, "Delivery Driver"),

)



ORDER_STATUS = (
    (1, "waiting"),
    (2, "ordered"),
    (3, "success"),
    (4, "cancel"),

)



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=10)
    point = models.IntegerField()
    
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(choices=EMP_POSITION)
    point = models.IntegerField()
    tel = models.CharField(max_length=10)
    address = models.TextField()


class Category(models.Model):
    category = models.CharField(max_length=255)
    
class Menu(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.BooleanField(default=1)
    

class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
class Zone(models.Model):
    name = models.CharField(max_length=8)
    
class Table(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=0)
    
class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    date = models.DateTimeField(auto_created=True)
    status = models.IntegerField(choices=ORDER_STATUS)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
