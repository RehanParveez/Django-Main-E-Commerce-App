from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from orders.forms import ShippingAddressForm
from orders.models import Order, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
import time
import stripe
from orders.keys import stripe
from django.urls import reverse
from django.conf import settings

# Create your views here.

class CheckoutInfoView(LoginRequiredMixin, View): 
    template_name = 'orders/checkout_info.html'
    
    def get(self, request):
        form = ShippingAddressForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ShippingAddressForm(request.POST)
        
        if form.is_valid():
            existing_order_id = request.session.get('order_id')
            if existing_order_id:
                order = Order.objects.get(id=existing_order_id)
            else:
                # Creating a new order with simple unique order_number
               order_number = f"ORD{int(time.time() * 1000)}"
               order = Order.objects.create(user=request.user if request.user.is_authenticated else None,
                  subtotal=0, shipping_cost=0, total=0, order_number=order_number)
               # storing order id in session
               request.session['order_id'] = order.id
            shipping = form.save(commit=False)
            shipping.order = order
            shipping.save()
            return redirect('checkout_payment')
       
        return render(request, self.template_name, {'form':form})
    
    
class CheckoutPaymentView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'orders/checkout_payment.html'

    def get(self, request):
        # Trying to get order from session first
        order_id = request.session.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
        else:
            # allowing the user to access the last order if session is expired
            order = Order.objects.filter(user=request.user).order_by('-created_at').first()
            if not order:
                return redirect('cart_detail')

        faqs = [
            {'question': 'Is my Credit Card / Debit Card details protected?',
             'answer': 'Yes, it is protected, don’t worry.'},
            {'question': 'Can I use a Debit Card to make payment?',
             'answer': 'It’s your card, do whatever you want with it.'},
            {'question': 'Credit Card/Debit Card transaction keeps failing. Why?',
             'answer': 'Maybe there is a glitch in the system which needs a fix.'},
            {'question': 'Did not receive the Pin Code on my mobile?',
             'answer': 'Oh sorry to hear that, try the transaction again to confirm.'},
            {'question': 'My credit card has been charged, but my order shows failed?',
             'answer': 'Don’t panic, maybe it’s just a delay due to system load.'},
        ]

        context = {
            'order': order,
            'shipping': order.shipping_address,
            'payment_methods': Payment.PAYMENT_METHODS,
            'faqs': faqs
        }

        return render(request, self.template_name, context)

    def post(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            return redirect('cart_detail')
        
        order = get_object_or_404(Order, id=order_id)
        method = request.POST.get('payment_method') or 'Card'

        # Creating or updating payment
        payment, created = Payment.objects.update_or_create(
            order=order,
            defaults={'method': method, 'amount': order.total, 'status': 'success'}
        )

        # Updating order payment status
        order.payment_status = 'paid'
        order.save()

        return redirect('checkout_complete')
    
    
class CheckoutCompleteView(LoginRequiredMixin, View):
    template_name = 'orders/checkout_complete.html'

    def get(self, request):
        order_id = request.session.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
        else:
            order = Order.objects.filter(user=request.user, payment_status='paid').order_by('-created_at').first()
            if not order:
                return redirect('cart_detail')
        context = {'order': order, 'shipping': order.shipping_address}

        # deleting session only if order was in session
        if order_id:
            del request.session['order_id']
        return render(request, self.template_name, context)
    
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        

class PaymentCheckoutView(LoginRequiredMixin, View):
    """Redirecting user to Stripe checkout for a given order."""
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)

        if order.payment_status == 'paid':
            return redirect('order_detail', pk=order.pk)

        # Creating Stripe checkout session
        session = stripe.checkout.Session.create( payment_method_types=['card'],
            line_items=[{'price_data': {
                    'currency': 'pkr', 'unit_amount': int(order.total * 100),  # the Stripe expects amount in cents
                    'product_data': {'name': f'Order {order.pk}'},
                    }, 'quantity': 1}],
            mode='payment', metadata={'order_id': order.pk},
            success_url=request.build_absolute_uri(
                reverse('payments_done', args=[order.pk])),
            cancel_url=request.build_absolute_uri(
                reverse('payments_cancel', args=[order.pk])),
        )
        return redirect(session.url)
