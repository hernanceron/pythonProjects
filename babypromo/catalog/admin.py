from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'store')
    list_filter = ('store',)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Store)
