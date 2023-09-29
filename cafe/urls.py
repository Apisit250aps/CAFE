from django.contrib import admin
from django.urls import include, path

from . import views as api

urlpatterns = [
    # register data api
    path('get/employee-position/', api.getEmployeePosition, name='api-get-employee-position'),
    path('get/province/', api.getProvince, name='api-get-province'),
    path('get/district/', api.getDistrict, name='api-get-district'),
    path('get/sub-district/', api.getTambon, name='api-get-sub-district'),
    
    # authentications 
    path('auth/register/', api.register, name='register-api'),
    
    
    # Order
    path('order/all', api.showOrderAll, name='api-all-order'),
    path('order/<int:id>', api.showOrderStatus, name='api-status-order'),
    path('order/create', api.sentOrder, name='api-sent-order'),
    path('order/accept', api.acceptOrder, name='api-accept-order'),
    path('order/success', api.orderSuccess, name='api-success-order'),
    path('order/cancel', api.cancelOrder, name='api-cancel-order'),
    
    # Product
    path('product/all', api.showProductAll, name='api-all-product')
    
    # cart 
]
