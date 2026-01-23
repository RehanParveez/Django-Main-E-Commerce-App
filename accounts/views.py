from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserForm, ProfileForm
from django.views.generic import TemplateView

# Create your views here.
class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'account  is created')
            return redirect('account_dashboard')
        return render(request, self.template_name, {'form': form})
    
class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(request.POST, instance=request.user.profile)
        
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request, 'profile is updated')
            return redirect('profile')
        
        return render(request, self.template_name, {'userform': userform, 'profileform': profileform})
        
class AccountDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'