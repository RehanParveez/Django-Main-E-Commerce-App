from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class CheckoutInfoView(TemplateView):
    template_name = 'orders/checkout_info.html'
    
class CheckoutPaymentView(TemplateView):
    template_name = 'orders/checkout_payment.html'
    
class CheckoutCompleteView(TemplateView):
    template_name = 'orders/checkout_complete.html'
