from django.urls import path
from main.views import about_us, home, contact_us, faq

urlpatterns = [
    path("", home, name='home'),
    path('aboutus/', about_us, name='about_us'),
    path('contactus/', contact_us, name='contact_us'),
    path('faq/', faq, name='faq'),
]
