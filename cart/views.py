from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from cart.models import Cart, CartItem, Products

# Create your views here.
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
    else:
        if not request.session.session_key:
            request.session.save()
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key,
            is_active=True)
    return cart

class CartDetailView(TemplateView):
    template_name = "cart/checkout_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        context["cart"] = cart
        context["cart_items"] = cart.cart_items.select_related('product')
        # handing current step logic
        context['current_step'] = 1
        return context
    
class CartAddView(View):
    def post(self, request):
        cart = get_cart(request)
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Products, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"price": product.price})

        if not created:
            item.quantity += 1
        item.save()
        return redirect("cart_detail")

class CartItemUpdateView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        # getting task from POST if exist
        task = request.POST.get('task')
        
        if task == "increase":
            item.quantity += 1
            item.save()

        elif task == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        return redirect("cart_detail")

class CartItemDeleteView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect("cart_detail")


class CheckoutInfoView(TemplateView):
    template_name = 'cart/checkout_cart.html'  # this view is just for rendering the checkout_info anchor tag given inside the checkout_cart.html will fix it later while working on the orders app and handling checkout_info part
    