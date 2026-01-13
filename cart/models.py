from django.db import models
from DjangoMainECommerce.models import BaseModel
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_key = models.CharField(max_length=35, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username if self.user else f'Guest Cart ({self.session_key})'
        
    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())
    
    def subtotal(self):
        return sum(item.item_total for item in self.cart_items.all())
    
    def shipping_price(self):
        return 0 #will change this later if shipping price needs to be charged
   
    def final_total(self):
        return self.subtotal() + self.shipping_price()


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} {self.quantity}"
    
    @property
    def item_total(self):
        return self.price * self.quantity
    
    
    