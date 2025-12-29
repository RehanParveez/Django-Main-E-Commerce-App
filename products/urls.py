from django.urls import path
from products.views import product_detail, product_list, product_search
 
urlpatterns = [
    path('productdetail/', product_detail, name='product_detail'),
    path('productlist/', product_list, name='product_list'),
    path('productsearch/', product_search, name='product_search'),
]
