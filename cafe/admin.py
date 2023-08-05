from django.contrib import admin

from . import models

# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )

    search_fields = (
        'category',
    )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'desc',
        'price',
        'category',
        'stock_level',
    )

