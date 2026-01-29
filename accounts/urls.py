from django.urls import path
from accounts.views import LoginView, LogoutView, RegisterView, ProfileView, AccountDashboardView, OrderHistoryView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', 
    email_template_name='accounts/password_reset_email.html'), name='password_reset'),
    path('passwordresetdone/', auth_views.PasswordResetDoneView.as_view(template_name= 'accounts/password_reset_done.html'), name='password_reset_done'),
    path("passwordresetconfirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("passwordresetcomplete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    
    path("passwordchange/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    
    path('accountdashboard/', AccountDashboardView.as_view(), name='account_dashboard'), 
     path('ordershistory/', OrderHistoryView.as_view(), name='order_history'),
]
