from django.urls import path
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
    path(
        "products/",
        views.ProductListView.as_view(),
        name="products",
    ),
    path(
        "load-products/",
        views.upload,
        name="upload"
    )
]