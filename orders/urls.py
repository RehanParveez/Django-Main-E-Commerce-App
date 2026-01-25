from django.urls import path
from orders.views import CheckoutInfoView, CheckoutPaymentView, CheckoutCompleteView, OrderDetailView

urlpatterns = [
    path('checkoutinfo/', CheckoutInfoView.as_view(), name='checkout_info'),
    path('checkoutpayment/', CheckoutPaymentView.as_view(), name='checkout_payment'),
    path('checkoutcomplete/', CheckoutCompleteView.as_view(), name='checkout_complete'),
    path('orderdetail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]

