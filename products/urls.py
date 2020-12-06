from django.urls import path
import products.views

urlpatterns = [
    path(r'vendors', products.views.VendorsController.as_view()),
    path(r'vendors/<int:id>', products.views.FetchVendorById.as_view()),
    path(r'vendors/<int:id>/products', products.views.ProductsByVendor.as_view()),
    path(r'products/<int:id>', products.views.ProductDetails.as_view()),
    path(r'products', products.views.ProductsController.as_view()),
]
