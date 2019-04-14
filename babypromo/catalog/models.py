from django.db import models
from datetime import date
from enum import Enum

# Create your models here.
class Brand(models.Model):
    INACTIVO = 'INA'
    ACTIVO = 'ACT'
    STATUS = (
        ( INACTIVO, 'Inactivo'),
        ( ACTIVO, 'Activo'),
    )
    name = models.CharField(max_length = 20, default = None)
    status = models.CharField(max_length = 3 ,
                              choices = STATUS,
                              default = ACTIVO,)
    def __str__(self):
        return '%s' % (self.name)


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length = 256, default = None)
    image_url = models.CharField(max_length = 256)
    principalCode = models.CharField(max_length = 10)
    def __str__(self):
        return '%s %s' % (self.name, self.brand)

class Store(models.Model):   
    INACTIVO = 'INA'
    ACTIVO = 'ACT'
    STATUS = (
        ( INACTIVO, 'Inactivo'),
        ( ACTIVO, 'Activo')
    )
    name = models.CharField(max_length = 20, default = None)
    status = models.CharField(max_length = 3 ,
                              choices = STATUS,
                              default = ACTIVO,)
    product = models.ManyToManyField(Product, through = 'Price')
    
    def __str__(self):
        return '%s' % (self.name)

class PriceManager(models.Manager):
    def get_queryset(self):
        q1 = super().get_queryset().filter(published_date = date.today())
        return q1

class Price(models.Model):
    published_date = models.DateField()
    price = models.CharField(max_length = 10)
    discount_price = models.CharField(max_length = 10)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    objects = models.Manager()
    active_prices = PriceManager()