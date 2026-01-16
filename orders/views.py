from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from orders.forms import ShippingAddressForm
from orders.models import Order, Payment

# Create your views here.

class CheckoutInfoView(View): 
    template_name = 'orders/checkout_info.html'
    
    def get(self, request):
        form = ShippingAddressForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ShippingAddressForm(request.POST)
        
        if form.is_valid():
           order = Order.objects.create(user=request.user if request.user.is_authenticated else None,
           subtotal=0, shipping_cost=0, total=0)
           
           shipping = form.save(commit=False)
           shipping.order = order
           shipping.save()
           # storing order id in session
           request.session['order_id'] = order.id
           return redirect('checkout_payment')
       
        return render(request, self.template_name, {'form':form})
    
    
class CheckoutPaymentView(View):
    template_name = 'orders/checkout_payment.html'
    
    def get(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            return redirect('cart_detail')
        order = get_object_or_404(Order, id=order_id)
        
        faqs = [
            {'question': 'Is my Credit Card / Debit Card details protected?',
             'answer': 'yes its protected, dont worry.'},
            {'question': 'Can I use a Debit Card to make payment?',
             'answer': 'its your card do whatever you want to do with it'},
            {'question': 'Credit Card/Debit Card transaction keep failing. Why?',
             'answer': 'maybe there is a glitch in the system which needs the fix.'},
            {'question': 'Did not receive the Pin Code on my mobile?',
             'answer': 'oh sorry to hear that, you should try the transaction process one time more, to confirm that its a permanent issue.'},
            {'question': 'My credit card has been charged, but my order shows failed?',
             'answer': 'ok, dont panic maybe its just a delay due to system load.'},
        ]
        
        context = {
            'order': order,
            'shipping': order.shipping_address,
            'payment_methods': Payment.PAYMENT_METHODS,
            'faqs': faqs}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            return redirect('cart_detail')
        order = get_object_or_404(Order, id=order_id)
        method = request.POST.get('payment_method') or 'Card'
        
        payment, created = Payment.objects.update_or_create(order=order, defaults={'method': method, 'amount': order.total,
        'status': 'success'})
        
        order.payment_status = 'paid'
        order.save()
        
        return redirect('checkout_complete')
    
    
class CheckoutCompleteView(View):
    template_name = 'orders/checkout_complete.html'
    
    def get(self, request):
        order_id = request.session.get('order_id')
        
        if not order_id:
            return redirect('cart_detail')
        order = get_object_or_404(Order, id=order_id)
        
        context = {
            'order': order,
            'shipping': order.shipping_address,
        }
        # deleting the session after success
        del request.session['order_id']
        return render(request, self.template_name, context)
        
