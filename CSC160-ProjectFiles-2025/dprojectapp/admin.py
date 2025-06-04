from django.contrib import admin
from .models import Product
from .models import Customer
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'mi', 'email', 'phone')


admin.site.register(Product, ProductAdmin)

admin.site.register(Customer, CustomerAdmin)

