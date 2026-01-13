from django.contrib import admin
from cart.models import Cart, CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'is_active']
    list_filter = ['is_active', 'user']
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'price', 'quantity', 'created_at']
    list_filter = ['cart', 'product']