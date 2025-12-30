from django.urls import path
from main.views import HomeView, AboutUsView, ContactUsView, FaqView

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path('aboutus/', AboutUsView.as_view(), name='about_us'),
    path('contactus/', ContactUsView.as_view(), name='contact_us'),
    path('faq/', FaqView.as_view(), name='faq'),
]
