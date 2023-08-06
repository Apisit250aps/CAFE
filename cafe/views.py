from . import models
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import json

# Create your views here.


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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def EmployeeRegister(request):
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']
    fname = request.data['fname']
    lname = request.data['lname']
    province = request.data['province']
    district = request.data['district']
    sub_district = request.data['sub_district']
    address = request.data['address']
    post_code = request.data['post_code']
    phone = request.data['phone']
    position = request.data['position']

    status = True

    try:
        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=username,
            email=email,
            password=password,
            is_staff=1
        )
        user.save()

        models.Employee.objects.create(
            user=user,
            address=address,
            sub_district=sub_district,
            district=district,
            province=province,
            post_code=post_code,
            phone=phone,
            position=position
        ).save()

    except:
        status = False
        User.objects.get(username=username).delete()
        
    return Response(
        {
            "status":status
        }
    )