from django.contrib import admin
from django.urls import include, path

from . import views as api

urlpatterns = [
    path('get/employee-position/', api.getEmployeePosition, name='api-get-employee-position'),
    path('get/province/', api.getProvince, name='api-get-province'),
    path('get/district/', api.getDistrict, name='api-get-district'),
    path('get/sub-district/', api.getTambon, name='api-get-sub-district'),
        
]
