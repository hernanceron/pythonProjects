from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
   list_display = [ 'name' , 'principalCode']
   list_filter = ('store__name',)

class PriceAdmin(admin.ModelAdmin):
   list_display = [ 'product', 'store' ]

admin.site.register(models.Store)
admin.site.register(models.Brand)
admin.site.register(models.Price, PriceAdmin)
admin.site.register(models.Product, ProductAdmin)

