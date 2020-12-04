from django.urls import path
import products.views

urlpatterns = [
    path('', products.views.index),
    path(r'v1/stores', products.views.VendorsController.as_view()),
    path(r'v1/products', products.views.ProductsController.as_view())
    #path(r'v1/stores', products.views.index),
]