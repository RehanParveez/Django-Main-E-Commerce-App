from django.urls import path
from cart.views import get_cart, CartDetailView, CartAddView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('getcart/', get_cart, name='get_cart'),
    path('cartdetail/', CartDetailView.as_view(), name='cart_detail'),
    path('cartadd/', CartAddView.as_view(), name='cart_add'),
    path('cartupdate/<int:item_id>/', CartItemUpdateView.as_view(), name='cart_update'),
    path('cartdelete/<int:item_id>/', CartItemDeleteView.as_view(), name='cart_delete'),
]
