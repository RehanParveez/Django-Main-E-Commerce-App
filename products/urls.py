from django.urls import path
from products.views import ProductListView, ProductDetailView, ProductSearchView, ProductReviewView, CategoryListView, SubcategoryListView
    
urlpatterns = [
    path('productlist/', ProductListView.as_view(), name='product_list'),
    path('productdetail/', ProductDetailView.as_view(), name='product_detail'), # for now detail url is without any pk or slug value because i am yet to fix all the template files to dynamic bcz they are static for now according to django templating requirement
    path('productsearch/', ProductSearchView.as_view(), name='product_search'),
    path('productreview/', ProductReviewView.as_view(), name='product_review'),
    path('categorylist/', CategoryListView.as_view(), name='category_list'),
    path('subcategorylist/', SubcategoryListView.as_view(), name='subcategory_list'),
]



