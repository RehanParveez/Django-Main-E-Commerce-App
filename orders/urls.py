from django.urls import path
from orders.views import CheckoutInfoView, CheckoutPaymentView, CheckoutCompleteView, OrderDetailView, StripeWebhookView

urlpatterns = [
    path('checkoutinfo/', CheckoutInfoView.as_view(), name='checkout_info'),
    path('checkoutpayment/', CheckoutPaymentView.as_view(), name='checkout_payment'),
    path('checkoutcomplete/', CheckoutCompleteView.as_view(), name='checkout_complete'),
    path('orderdetail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('paymentcheckout/<int:order_id>/', PaymentCheckoutView.as_view(), name='payment_checkout'),
    path('stripewebhook/', StripeWebhookView.as_view(), name='stripe_webhook')
]

