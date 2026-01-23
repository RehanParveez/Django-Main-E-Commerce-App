from django import forms
from accounts.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profileimage']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserForm(forms.ModelForm):
    class Meta:
       model = User
       fields = ['first_name', 'last_name', 'email']
        
