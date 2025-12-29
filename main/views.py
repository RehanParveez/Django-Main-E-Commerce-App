from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'main/parent.html')

def about_us(request):
    return render(request, 'main/about_us.html')
    
def contact_us(request):
    return render(request, 'main/contact_us.html')

def faq(request):
    return render(request, 'main/faq.html')