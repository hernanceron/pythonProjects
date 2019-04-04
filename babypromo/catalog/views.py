from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from catalog import models

# Create your views here.
class ProductListView(ListView):
    template_name="catalog/product_list.html"
    queryset = models.Product.objects.active()
    context_object_name="products"
    paginate_by=10