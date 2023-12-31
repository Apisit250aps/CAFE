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
