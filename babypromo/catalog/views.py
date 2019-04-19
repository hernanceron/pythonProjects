from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from catalog import models
from django import forms
import datetime

# Create your views here.

class LoaderForm(forms.Form):
    file = forms.FileField()

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(models.Product, principalCode=kwargs['pk'])  
        lista = models.Price.active_prices.all().filter(product__principalCode = product.principalCode)        
        context = {'producto' : product, 'lista': lista}
        return render(request, 'catalog/product_detail.html', context)

def product_list_by_store(request):
    storeid = request.GET.get('storeId')
    if storeid != None:
        products = models.Product.objects.filter( store__id = storeid )    
    else:
        products = models.Product.objects.all()
      
    return render(request,
                  "catalog/product_list.html",
                  {'products' : products}  )

def upload(request):
    if request.method == 'POST':
        form = LoaderForm(request.POST, request.FILES)

        def product_func(row):
            print(row[2])
            nameBrand = row[2]
            brand = models.Brand.objects.get( name= nameBrand.upper() )
            if brand == None:
                brand = models.Brand.create( nameBrand.upper(), 'ACT')
            row[2] = brand
            return row

        def price_func(row):
            print(row[0])
            cadena = row[0]
            longitud = len(cadena)
            if longitud == 6:
                year = cadena[ 0:4 ]
                month = cadena[ 4:5 ]
                day = cadena[ 5:6 ]
            elif longitud == 7:
                year = cadena[ 0:4 ]
                month = cadena[ 4:5 ]
                day = cadena[ 5:7 ]
            
            fecha = datetime.datetime(int(year), int(month), int(day))
            row[0] = fecha

            print(row[7])
            codBabyPromo = row[7]
            producto = models.Product.objects.filter( principalCode = codBabyPromo )[0]
            row[7] = producto

            return row

        if form.is_valid():            
            request.FILES['file'].save_to_database(
                model = models.Product,
                initializer = product_func,
                mapdict = ['name', 'internalCode' , 'brand', 'typeProduct', 'model', 'size', 'quantity', 'presentation', 'principalCode', 'image_url']
                )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
    else:
        form = LoaderForm()
    return render(
        request,
        'catalog/load.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                    'from your cloned repository:')
        })
