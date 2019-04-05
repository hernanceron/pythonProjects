from django import forms
from models import Product, Store

class LoaderForm(forms.Form):
    name = forms.FileField()

def upload(request):
    if request.method == 'POST':
        form = LoaderForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
        def store_func(row):
            print(row[7])
            s = Store.objects.filter(name=row[7])[0]
            row[7] = s
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[
                    (Product, ['published_date', 'name', 'code', 'brandName', 'image_url', 'price', 'discount_price', 'store', 'principalCode'], store_func, 0)
                 ]
                )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
