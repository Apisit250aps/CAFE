from . import serializers
from . import models

def Choice(id:int, choices:tuple):
    
    for os in choices:
        if os[0] == id:
            return os


def Employee(id:int):
    
    return serializers.EmployeeSerializer(models.Employee.objects.get(id=id)).data
    
def Customer(id:int):

    return serializers.CustomerSerializer(models.Customer.objects.get(id=id)).data
    
def Product(id:int):

    return serializers.ProductSerializer(models.Product.objects.get(id=id)).data
    