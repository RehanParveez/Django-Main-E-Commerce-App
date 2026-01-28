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

def popular_mobile_products(request):
    mobile_category = Category.objects.filter(name__iexact="Mobile Phones", is_active=True).first()
    products = (
        Products.objects.filter(category=mobile_category, is_active=True, quantity__gt=0).select_related(
        'category', 'subcategory').prefetch_related('images')[:20] if mobile_category else []
        )
    return {
        "popular_mobile_products": products}

def all_subcategories(request):
    subcategories = SubCategory.objects.filter(is_active=True)
    return {'subcategories': subcategories}

def cart_context(request):
    cart = get_cart(request)
    cart_items = cart.cart_items.select_related('product')
    return {'cart': cart, 'cart_items': cart_items}

