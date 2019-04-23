from django.urls import path, re_path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from catalog import views


urlpatterns = [
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about-us",
    ),
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
    re_path(r'^products$',
        views.product_list_by_store,
        name = "productsStore"),
    path(
        "load-products/",
        views.upload_products,
        name="upload_products"
    ),
    path(
        "load-prices/",
        views.upload_prices,
        name="upload_prices"
    ),
    re_path(
        r'^products/(?P<pk>\w+)/$',       
        views.ProductDetailView.as_view(),
        name="productsDetails"
    ),
    re_path(r'^stores/(?P<storeId>\d+)/$',
        views.product_list_by_store,
        name = "storeDetails"),
  
]