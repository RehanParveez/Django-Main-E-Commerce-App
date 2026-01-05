from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from products.models import Products, Category, SubCategory, ProductImage, ProductFeature, ProductReview
# Create your views here.

class ProductListView(ListView):
    model = Products
    template_name = 'products/product.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Products.objects.filter(is_active=True)


class ProductDetailView(DetailView):  # have passed listiew just htat my pages simply run because detail view requires passing of pk or slug in urls which i have not done becuase products are not added and further logic is simple.
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # product = Products.objects.first()  # temporary fix bcz of use of listview instead of detail view above
        context['images'] = self.object.images.all()
        context['features'] = self.features.all()
        context['reviews'] = self.reviews.all()
        return context


class ProductSearchView(ListView):  
    model = Products
    template_name = 'products/search_results.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if not query:
            return Products.objects.none()
        return Products.objects.filter(name__icontains=query, is_active=True)
        
    
class ProductReviewView(ListView): 
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        ProductReview.objects.create(product=self.object, name = request.POST.get('name'), title = request.POST.get('title'),
        review = request.POST.get('review'), rating = request.POST.get('rating'))
        return redirect('product_detail', pk=self.object.pk)
    

class CategoryListView(ListView):
     model = Category
     template_name = 'products/product.html'
     context_object_name = 'products'
     
     def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Products.objects.filter(category = self.category, is_active=True)

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
     
     
class SubcategoryListView(ListView): 
    model = SubCategory
    template_name = 'products/product.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        self.subcategory = get_object_or_404(SubCategory, slug=self.kwargs['slug'], is_active=True)
        return Products.objects.filter(subcategory = self.subcategory, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        return context
        

    