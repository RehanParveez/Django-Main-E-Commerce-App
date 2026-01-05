from products.models import Products

def default_product(request):
    product = Products.objects.filter(is_active=True).first()
    return{'product': product}

