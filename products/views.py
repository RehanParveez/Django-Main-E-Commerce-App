from django.shortcuts import render

# Create your views here.
def product_detail(request):
    return render(request, 'products/product_detail.html')

def product_list(request):
    return render(request, 'products/product.html')

def product_search(request):
    return render(request, 'products/search_results.html')