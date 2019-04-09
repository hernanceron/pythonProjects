from django.db import models


# Create your models here.
class Store(models.Model):
    STATUS_CHOICE = (
        ('inactivo' ,  'Inactivo'),
        ('activo' , 'Activo'),
    )
    name = models.CharField(max_length = 20)
    status = models.CharField(max_length = 20 ,
                              choices = STATUS_CHOICE,
                              default = 'activo')
    
    def __str__(self):
        return '%s' % (self.name)

class ProductManager(models.Manager):
    def active(self):
        return self.filter(store__status='activo').order_by("name")
    
    def anotherStores(self,principalCode):
        return self.filter(principalCode = principalCode).order_by("name")

class Product(models.Model):
    published_date = models.DateField()
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=100)
    brandName = models.CharField(max_length=100)
    image_url = models.CharField(max_length=256)
    price = models.CharField(max_length = 10)
    discount_price = models.CharField(max_length = 10)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    principalCode = models.CharField(max_length = 20)

    objects = ProductManager()

    def __str__(self):
        return '%s %s' % (self.name, self.store)