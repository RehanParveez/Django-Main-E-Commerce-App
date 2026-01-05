from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View
from main.models import ContactUs
from products.models import Category, SubCategory, Products
from django.urls import reverse_lazy
# Create your views here.

class HomeView(View):
    def get(self, request, **kwargs):
        category = Category.objects.filter(is_active = True)
        subcategory = SubCategory.objects.filter(is_active = True)
        
        popular_products = (Products.objects.filter(
            is_active=True, quantity__gt=0).select_related('category', 'subcategory').prefetch_related('images')[:20])
        
        Item_per_columns = 5
        Popular_phone_columns = []
    
        for i in range(0, len(popular_products), Item_per_columns):
            column = popular_products[i:i+ Item_per_columns]
            Popular_phone_columns.append(column)
    
        return render(request, 'main/index.html', {'category': category, 'subcategory':subcategory,
           'popular_products':popular_products, 'popular_phone_columns':Popular_phone_columns})
    
    
class AboutUsView(TemplateView):
    template_name = 'main/about_us.html'
    
class ContactUsView(CreateView):
    template_name = 'main/contact_us.html'
    model = ContactUs
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('contact_us')

class FaqView(TemplateView):
    template_name = 'main/faq.html'