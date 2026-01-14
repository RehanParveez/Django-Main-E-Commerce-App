from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
class Order(models.Model):
    
    STATUS_CHOICES = ( 
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    )
    
    PAYMENT_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    order_number = models.CharField(max_length=25, unique=True, blank=True)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='unpaid')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.order_number or self.id}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.product} {self.quantity}"
    
    
class ShippingAddress(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='shipping_address')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    company_name = models.CharField(max_length=60, blank=True)
    
    area_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    street_address_1 = models.CharField(max_length=240)
    street_address_2 = models.CharField(max_length=240)
    zip_code = models.CharField(max_length=20)
    is_business = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Payment(models.Model):
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('paypal', 'Paypal'),
        ('stripe', 'Stripe'),
        ('cod', 'Cash on Delivery'),
    )
    
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=25, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=25, choices=(('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.order.id}"