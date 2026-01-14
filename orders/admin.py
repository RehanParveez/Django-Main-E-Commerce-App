from django.contrib import admin
from orders.models import Order, OrderItem, ShippingAddress, Payment

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'status', 'order_number', 'payment_status', 'shipping_cost']
    list_filter = ['status', 'payment_status', 'order_number']
      
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order', 'product', 'quantity']
    
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['order', 'first_name', 'last_name', 'company_name', 'area_code', 'phone', 'zip_code']
    list_filter = ['first_name', 'last_name', 'phone']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'amount', 'status', 'created_at']
    list_filter = ['method', 'status']
