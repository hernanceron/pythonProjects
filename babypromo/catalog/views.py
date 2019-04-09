from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from catalog import models
from django import forms

# Create your views here.
class ProductListView(ListView):
    template_name="catalog/product_list.html"
    queryset = models.Product.objects.active()
    context_object_name="products"
    paginate_by=3

class LoaderForm(forms.Form):
    file = forms.FileField()

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(models.Product, code=kwargs['pk'])  
        lista = models.Product.objects.anotherStores(product.principalCode)
        context = {'producto' : product, 'lista': lista}
        return render(request, 'catalog/product_detail.html', context)

def upload(request):
    if request.method == 'POST':
        form = LoaderForm(request.POST, request.FILES)

        def store_func(row):
            print(row[7])
            s = models.Store.objects.filter(name=row[7])[0]
            row[7] = s
            return row

        if form.is_valid():            
            request.FILES['file'].save_to_database(
                model = models.Product,
                initializer = store_func,
                mapdict = ['published_date', 'name', 'code', 'brandName', 'image_url', 'price', 'discount_price', 'store', 'principalCode']
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
