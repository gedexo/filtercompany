from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("products/", views.products, name="products"),
    path("products/category/<slug:slug>/", views.products_by_category, name="products_by_category"),
    path("product/<slug:slug>/", views.product_details, name="product_details"),
    path("blog/", views.blog, name="blog"),
    path("blog-details/<slug:slug>", views.blog_details, name="blog-details"),
    path("contact/", views.contact, name="contact"),
    path("PET/index.html/", views.iframe_view, name="iframe-page"),
    path("PET/", lambda request: redirect("web:iframe-page", permanent=True)),
    # redirects
]
