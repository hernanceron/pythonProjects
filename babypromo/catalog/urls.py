from django.urls import path, re_path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from catalog.views import ProductListView, ProductDetailView
from catalog import views


urlpatterns = [
    path(
        '',
        ProductListView.as_view(),
        name = 'products' ),
    path('<pk>',ProductDetailView.as_view(), name= 'product_details'),
  
]