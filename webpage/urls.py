from django.contrib import admin
from django.urls import path

from . import views as page

urlpatterns = [
    path('', page.index, name='index'),
    path('staff/employee/create/', page.EmployeeCreatePage, name='create-employee-page')
]