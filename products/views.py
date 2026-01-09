from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from products.models import Products, Category, SubCategory, ProductReview
# Create your views here.

class ProductListView(ListView):
    model = Products
    template_name = 'products/product.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Products.objects.filter(is_active=True)


class ProductDetailView(DetailView):  
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['images'] = product.images.all()
        context['features'] = product.features.all()
        context['reviews'] = product.reviews.all()
        context['specifications'] = product.specifications.all()
        context['similar_products'] = Products.objects.filter(category=product.category, is_active=True).exclude(
            pk=product.pk)[:6]
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
        
    
class ProductReviewView(View): 

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=kwargs.get('pk'))
        
        ProductReview.objects.create(product=product, name = request.POST.get('name'), title = request.POST.get('title'),
        review = request.POST.get('review'), rating = int(request.POST.get('rating', 1)))
        return redirect('product_detail', pk=product.pk)
        

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
        

    