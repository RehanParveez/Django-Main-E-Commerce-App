from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View
from main.models import ContactUs
from products.models import Category, SubCategory, Products
from django.urls import reverse_lazy
# Create your views here.

class HomeView(View):
    def get(self, request, **kwargs):
        categories = Category.objects.filter(is_active = True)
        subcategories = SubCategory.objects.filter(is_active = True)
        
        slider_products = Products.objects.filter(
            is_active=True, is_featured=True).select_related('category', 'subcategory').prefetch_related('images')[:3]
        
        promotion_products = Products.objects.filter(
            is_active=True, is_promotion=True).select_related('category', 'subcategory').prefetch_related('images')[:10]
        
        featured_product = Products.objects.filter(
            is_active=True, is_featured=True).select_related('category', 'subcategory').prefetch_related('images')[:10]
        
        trending_products = Products.objects.filter(
            is_active=True, is_trending=True).select_related('category', 'subcategory').prefetch_related('images')[:6]
        
        mobile_category = Category.objects.filter(name__iexact="Mobile Phones", is_active=True).first()
        popular_mobile_products = Products.objects.filter(
            category=mobile_category, is_active=True, quantity__gt=0).select_related('category', 'subcategory').prefetch_related(
            'images')[:20] if mobile_category else []
            
        tablet_category = Category.objects.filter(name__iexact="Tablets", is_active=True).first()
        
        mobile_products = mobile_category.products.filter(is_active=True, quantity__gt=0).prefetch_related('images') if mobile_category else []
        tablet_products = tablet_category.products.filter(is_active=True, quantity__gt=0).prefetch_related('images') if tablet_category else []
        
        
        return render(request, 'main/index.html', {'categories': categories, 'subcategories':subcategories,
           'popular_mobile_products':popular_mobile_products, 'slider_products':slider_products, 'promotion_products':promotion_products,
            'featured_product':featured_product, 'trending_products':trending_products, 'mobile_products':mobile_products,
            'tablet_products':tablet_products})
        
    
class AboutUsView(TemplateView):
    template_name = 'main/about_us.html'
    
class ContactUsView(CreateView):
    template_name = 'main/contact_us.html'
    model = ContactUs
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('contact_us')

class FaqView(TemplateView):
    template_name = 'main/faq.html'
    
