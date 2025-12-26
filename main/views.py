from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'main/parent.html', name='home')

def about_us(request):
    return render(request, 'main/about_us.html', name='about')
    
def contact_us(request):
    return render(request, 'main/contact_us.html', name='contact')

def faq(request):
    return render(request, 'main/faq.html', name='faq')