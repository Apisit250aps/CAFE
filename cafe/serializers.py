from rest_framework import serializers

from . import models

all = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = all
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = all
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = all
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = all