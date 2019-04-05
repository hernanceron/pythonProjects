from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from catalog import models
from django import forms

# Create your views here.
class ProductListView(ListView):
    template_name="catalog/product_list.html"
    queryset = models.Product.objects.active()
    context_object_name="products"
    paginate_by=10

class LoaderForm(forms.Form):
    file = forms.FileField()

def upload(request):
    if request.method == 'POST':
        form = LoaderForm(request.POST, request.FILES)

        def store_func(row):
            print(row[7])
            s = models.Store.objects.filter(name=row[7])[0]
            row[7] = s
            return row

        if form.is_valid():            
            request.FILES['file'].save_book_to_database(
                models=[
                    (models.Product, ['published_date', 'name', 'code', 'brandName', 'image_url', 'price', 'discount_price', 'store', 'principalCode'], store_func, 0)
                 ]
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
