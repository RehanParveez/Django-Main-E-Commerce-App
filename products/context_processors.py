from products.models import Products

def default_product(request):
    products = Products.objects.filter(is_active=True).first()
    return{'products': products}

def latest_products(request):
    products = Products.objects.filter(is_active=True).order_by('-id')[:4]
    return{'latest_products': products}

