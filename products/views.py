from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from products.models import Products, Category, SubCategory, ProductReview
from django.db.models import Count, Q
# Create your views here.

class ProductListView(ListView):
    model = Products
    template_name = 'products/product.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        qs = Products.objects.filter(is_active=True)
        q = self.request.GET.get('q', '')
        category = self.request.GET.get('category', None)
        price_from = self.request.GET.get('price_from', None)
        price_to = self.request.GET.get('price_to', None)
        
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        if price_from:
            qs = qs.filter(price__gte=price_from)
        if price_to:
            qs = qs.filter(price__lte=price_to)
        return qs.prefetch_related('images').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).annotate(
        active_products_count=Count('products', filter=Q(products__is_active=True)))
        
        # passing current filters for pagination links
        context['q'] = self.request.GET.get('q', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['price_from'] = self.request.GET.get('price_from', '')
        context['price_to'] = self.request.GET.get('price_to', '')
        return context


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
    paginate_by = 9
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        category_id = self.request.GET.get('category')
        
        products = Products.objects.filter(is_active=True, quantity__gt=0).select_related(
            'category', 'subcategory').prefetch_related('images').distinct()
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(subcategory__name__icontains=query))
        if price_from:
            products = products.filter(price__gte=price_from)
        if price_to:
            products = products.filter(price__lte=price_to)

        # filtering category
        if category_id:
            products = products.filter(category__id=category_id)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passing current filters to template
        context['query'] = self.request.GET.get('q', '')
        context['price_from'] = self.request.GET.get('price_from', '')
        context['price_to'] = self.request.GET.get('price_to', '')
        context['category_id'] = self.request.GET.get('category', '')
        context['categories'] = Category.objects.annotate(
        active_products_count=Count('products', filter=Q(products__is_active=True, products__quantity__gt=0)))

        # total results count
        context['result_count'] = self.get_queryset().count()
        return context
        
    
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
        context['categories'] = Category.objects.filter(is_active=True)
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
        context['categories'] = Category.objects.filter(is_active=True)
        return context
        

    