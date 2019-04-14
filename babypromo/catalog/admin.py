from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
   list_filter = ('store__name',)

admin.site.register(models.Store)
admin.site.register(models.Brand)
admin.site.register(models.Price)
admin.site.register(models.Product, ProductAdmin)

