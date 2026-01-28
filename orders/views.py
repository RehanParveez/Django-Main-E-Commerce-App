from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.forms import ShippingAddressForm
from orders.models import Order, ShippingAddress, Payment
from cart.views import get_cart
import time
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from cart.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutInfoView(LoginRequiredMixin, View):
    template_name = 'orders/checkout_info.html'

    def get(self, request):
        form = ShippingAddressForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            order_id = request.session.get('order_id')
            order = None

            if order_id:
                order = Order.objects.filter(id=order_id, user=request.user, payment_status='unpaid').first()

            if not order:
                order = Order.objects.filter(user=request.user, payment_status='unpaid').order_by('-created_at').first()

            if not order:
                order_number = f"ORD{int(time.time() * 1000)}"
                order = Order.objects.create(
                    user=request.user, order_number=order_number)
            request.session['order_id'] = order.id

            if not order.order_items.exists():
                cart = get_cart(request)  # implement this function in your cart app
                if not cart or not cart.cart_items.exists():
                   return redirect('cart_detail')
                order.populate_from_cart(cart)

            shipping, created = ShippingAddress.objects.get_or_create(order=order)
            for field, value in form.cleaned_data.items():
                setattr(shipping, field, value)
            shipping.save()
            return redirect('checkout_payment')

        return render(request, self.template_name, {'form': form})

class CheckoutPaymentView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'orders/checkout_payment.html'

    def get(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            return redirect('cart_detail')

        order = Order.objects.filter(id=order_id, user=request.user, payment_status='unpaid').first()

        if not order:
            return redirect('cart_detail')

        if not order.order_items.exists():
            return redirect('cart_detail')
        order.recalculate_totals()

        # handling stripe payment intent
        intent = stripe.PaymentIntent.create(amount=int(order.total * 100), currency='pkr',
            metadata={
                'order_id': order.id,
                'user_id': request.user.id},
            automatic_payment_methods={'enabled': True},
        )

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
            'shipping': getattr(order, 'shipping_address', None),
            'payment_methods': Payment.PAYMENT_METHODS,
            'faqs': faqs,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret,
        }
        return render(request, self.template_name, context)

    
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

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=settings.STRIPE_WEBHOOK_SECRET)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        except ValueError:
            return HttpResponse(status=400)

        # logic for paymentintent succeeded
        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            order_id = intent["metadata"].get("order_id")

            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            # Idempotency check
            if order.payment_status != "paid":
                order.payment_status = "paid"
                order.status = "processing"
                order.transaction_reference = intent.get("id")
                order.save()

                Payment.objects.get_or_create( order=order,
                    defaults={"method": "stripe", "amount": order.total, "status": "success"},
                )
                try:
                    cart = Cart.objects.get(user=order.user, is_active=True)
                    cart.cart_items.all().delete()
                    cart.is_active=False
                    cart.save()
                except Cart.DoesNotExist:
                    pass
        return HttpResponse(status=200)


