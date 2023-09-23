from . import models
from . import serializers
from . import map


from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.contrib.auth import login, logout, authenticate


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import json


# Create your views here.

# Data for register


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getProvince(request):
    data = {}
    msg = 'already get thai province'

    result = finders.find('data/json/ProvinceThai.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    data['province'] = province.keys()

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['province'],
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getDistrict(request):
    data = {}
    msg = 'already get thai district'
    print(request.data['province'])

    result = finders.find('data/json/ProvinceThai.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    data['district'] = province[province_selected].keys()

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['district'],
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getTambon(request):
    data = {}
    msg = 'already get thai tambon'

    # get thai province file
    result = finders.find('data/json/ProvinceThai.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    district_selected = request.data['district']

    data['sub_district'] = province[province_selected][district_selected]

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['sub_district']
        }
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getEmployeePosition(request):
    position = models.EMP_POSITION

    return Response({
        "status": True,
        "data": list(position)
    })


# Authentications

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    status = True
    message = ""
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']

    no_Exist = (
        (User.objects.filter(username=username).count() == 0)
        and
        (User.objects.filter(email=email).count() == 0)
    )
    if no_Exist:
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        if user:
            auth = authenticate(
                username=username,
                password=password
            )
            login(request, auth)
            status = True
            message = "Success"
    else:
        status = False
        message = "Username or Email is exist!"

    return Response(
        {
            "status": status,
            "message": message
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def createCustomer(request):
    status = True
    message = ""

    user = User.objects.get(username=request.user.username)

    fname = request.data['fname']
    lname = request.data['lname']

    address = request.data['address']
    sub_district = request.data['sub_district']
    district = request.data['district']
    province = request.data['province']
    post_code = request.data['post_code']
    phone = request.data['phone']

    User.objects.filter(id=user.id).update(first_name=fname, last_name=lname)

    customer = models.Customer.objects.create(
        user=user,
        address=address,
        sub_district=sub_district,
        district=district,
        province=province,
        post_code=post_code,
        phone=phone,
    )

    if customer:
        status = True
        message = "Success"
    else:
        status = False
        message = "Fail"
    return Response(
        {
            "status": status,
            "message": message
        }
    )




# ========================================================================
# Order

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def showOrderAll(request):
    order = models.Order.objects.all().order_by('order_status')
    orderSerializer = serializers.OrderSerializer(order, many=True).data
    data = []
    for item in orderSerializer:
        item = dict(item)
        item['customer'] = map.Customer(item['customer'])
        item['employee'] = map.Employee(item['employee'])
        item['product'] = map.Product(item['product'])
        item['order_status'] = map.Choice(
            id=item['order_status'], choices=models.ORDER_STATUS)
        data.append(item)

    return Response(
        {
            "status": True,
            "data": data
        }
    )

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def showOrderStatus(request, id:int):
    order = models.Order.objects.filter(order_status=id).order_by('id')
    orderSerializer = serializers.OrderSerializer(order, many=True).data
    data = []
    for item in orderSerializer:
        item = dict(item)
        item['customer'] = map.Customer(item['customer'])
        item['employee'] = map.Employee(item['employee'])
        item['product'] = map.Product(item['product'])
        item['order_status'] = map.Choice(
            id=item['order_status'], choices=models.ORDER_STATUS)
        data.append(item)

    return Response(
        {
            "status": True,
            "data": data
        }
    )



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sentOrder(request):
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)
    product_object = json.loads(request.data['product_object'])

    for products in product_object.values():
        product = models.Product.objects.get(id=int(products['product_id']))
        quantity = int(products['quantity'])
        price = float(products['price'])
        try:
            
            models.Order.objects.create(
                customer=customer,
                product=product,
                quantity=quantity,
                price=price,
                order_status=1
            )
            status = True
            
        except Exception as err:
            status = False
            print(err)

    return Response(
        {
            "status": status
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def acceptOrder(request):
    user = User.objects.get(username=request.user.username)
    employee = models.Employee.objects.get(user=user)
    try :
        models.Order.objects.filter(id=request.data['order_id']).update(
            employee=employee,
            order_status=2
        )
        status = True
    except Exception as err:
        status = False
        print(err)
        
    return Response(
        {
            "status":status
        }
    )

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def orderSuccess(request):
    id = request.data['order_id']
    try :
        models.Order.objects.filter(id=id).update(
            order_status=3
        )
        status = True
    except Exception as err:
        status = False
        print(err)
        
    return Response(
        {
            "status":status
        }
    )

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def cancelOrder(request):
    id = request.data['order_id']
    try :
        models.Order.objects.filter(id=id).update(
            order_status=4
        )
        status = True
    except Exception as err:
        status = False
        print(err)
        
    return Response(
        {
            "status":status
        }
    )