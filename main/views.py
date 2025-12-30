from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from main.models import ContactUs
from django.urls import reverse_lazy
# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/parent.html'

class AboutUsView(TemplateView):
    template_name = 'main/about_us.html'
    
class ContactUsView(CreateView):
    template_name = 'main/contact_us.html'
    model = ContactUs
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('contact_us')

class FaqView(TemplateView):
    template_name = 'main/faq.html'