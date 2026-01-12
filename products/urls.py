from django.urls import path
from products.views import ProductListView, ProductDetailView, ProductSearchView, ProductReviewView, CategoryListView, SubcategoryListView
   
urlpatterns = [
    path('productlist/', ProductListView.as_view(), name='product_list'),
    path('productdetail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'), 
    path('productsearch/', ProductSearchView.as_view(), name='product_search'),
    path('productreview/<int:pk>/', ProductReviewView.as_view(), name='product_review'),
    path('categorylist/<slug:slug>', CategoryListView.as_view(), name='category_list'),
    path('subcategorylist/', SubcategoryListView.as_view(), name='subcategory_list'),
]

