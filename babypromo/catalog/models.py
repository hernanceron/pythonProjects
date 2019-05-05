from django.db import models
from datetime import date
from enum import Enum
from django.urls import reverse

# Create your models here.
class BrandManager(models.Manager):
    def get_queryset(self):
        q1 = super().get_queryset().filter(status = 'ACT')
        return q1
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
    objects = models.Manager()
    active_brands = BrandManager()
    def __str__(self):
        return '%s' % (self.name)

class TypeManager(models.Manager):
    def get_queryset(self):
        q1 = super().get_queryset().filter(status = 'ACT')
        return q1

class Type(models.Model):
    INACTIVO = 'INA'
    ACTIVO = 'ACT'
    STATUS = (
        ( INACTIVO, 'Inactivo'),
        ( ACTIVO, 'Activo'),
    )
    name = models.CharField(max_length = 50 , default = None)
    status = models.CharField(max_length = 3 ,
                                choices = STATUS,
                                default = ACTIVO,)
    objects = models.Manager()
    active_types = TypeManager()

class ModelsManager():
    def get_queryset(self):
        q1 = super().get_queryset().filter(status = 'ACT')
        return q1

class Modelo(models.Model):
    INACTIVO = 'INA'
    ACTIVO = 'ACT'
    STATUS = (
        ( INACTIVO, 'Inactivo'),
        ( ACTIVO, 'Activo'),
    )
    name = models.CharField(max_length = 60 , default = None)
    status = models.CharField(max_length = 3 ,
                                choices = STATUS,
                                default = ACTIVO,)
    objects = models.Manager()
    modelos_activos = ModelsManager()

class Product(models.Model):
    name = models.CharField(max_length = 256, default = None)   #nombreProducto
    internalCode = models.CharField(max_length = 20, default = None) #codigo
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)   #marca 
    typeProduct = models.ForeignKey(Type, on_delete = models.CASCADE, null = True)   
    #typeProduct = models.CharField(max_length = 5, default = None)  #Tipo
    model = models.CharField(max_length = 20, default = None) #Modelo
    size = models.CharField(max_length = 5, default = None) #size
    quantity = models.IntegerField(default = 0) #quantity
    presentation = models.CharField(max_length = 5, default = None) #presentation
    principalCode = models.CharField(max_length = 10, default = None)  #CodBaby  
    image_url = models.CharField(max_length = 256, default = None)     #web   
        
    def __str__(self):
        return '%s %s' % (self.principalCode, self.name)

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
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('storeDetails',
                        args=[self.id])

    def __str__(self):
        return '%s' % (self.name)

class PriceManager(models.Manager):
    def get_queryset(self):
        q1 = super().get_queryset().filter(published_date = date.today())
        return q1

class Price(models.Model):
    published_date = models.DateField()  #fecha
    price = models.CharField(max_length = 10)  #precio
    discount_price = models.CharField(max_length = 10)   #precioOferta
    store = models.ForeignKey(Store, on_delete = models.CASCADE)   #Web
    product = models.ForeignKey(Product, on_delete = models.CASCADE)  #CodBabypromo
    objects = models.Manager()
    active_prices = PriceManager()