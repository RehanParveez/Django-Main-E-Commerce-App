from products.models import Products
from products.models import Category, SubCategory
from cart.views import get_cart

def default_product(request):
    products = Products.objects.filter(is_active=True).first()
    return{'products': products}

def latest_products(request):
    products = Products.objects.filter(is_active=True).order_by('-id')[:4]
    return{'latest_products': products}

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return {'categories': categories}

def all_subcategories(request):
    subcategories = SubCategory.objects.filter(is_active=True)
    return {'subcategories': subcategories}

def cart_context(request):
    cart = get_cart(request)
    cart_items = cart.cart_items.select_related('product')
    return {'cart': cart, 'cart_items': cart_items}

