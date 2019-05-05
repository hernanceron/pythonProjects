from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import get_object_or_404
from catalog import models
from django import forms
from catalog.models import Product,Brand,Type, Modelo
import datetime

# Create your views here.

class LoaderForm(forms.Form):
    file = forms.FileField()
    
#muestra el detalle del producto elegido
class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(models.Product, principalCode=kwargs['pk'])        
        listaHistorico = models.Price.objects.filter(product__principalCode = product.principalCode).order_by('-published_date')[:7]

        listaActual = models.Price.active_prices.filter(product__principalCode = product.principalCode)

        context = {'producto' : product, 'lista': listaActual, 'listaHistorico': listaHistorico}
        return render(request, 'catalog/product_detail.html', context)

#lista todos los productos
class ProductListView(generic.ListView):
    queryset = Product.objects.order_by('name')
    context_object_name = 'products'
    paginate_by = 10
    template_name = "catalog/product_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = Brand.active_brands.all()
        context['type_list'] = Type.active_types.all()
        context['models_list'] = Modelo.modelos_activos.all()

        return context


class ProductSearchListView(generic.ListView):
    model = Product
    paginate_by = 10
    template_name = "catalog/product_list.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('productName')
      
        if keyword:
            return  Product.objects.filter(name__icontains = keyword)
        return queryset

def upload_prices(request):
    if request.method == 'POST':
        form = LoaderForm(request.POST, request.FILES)

        def price_func(row):
            print(row[0])
            cadenaInt = row[0]
            cadena = str(cadenaInt)
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

            nombreStore = row[3]
            store = models.Store.objects.get( name = nombreStore.upper() )
            row[3] = store

            print(row[4])
            codBabyPromo = row[4]
            producto = models.Product.objects.get( principalCode = codBabyPromo )
            row[4] = producto

            return row
        
        if form.is_valid():
            request.FILES['file'].save_to_database(
                model = models.Price,
                initializer = price_func,
                mapdict = ['published_date', 'price', 'discount_price', 'store', 'product']
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

def upload_products(request):
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
