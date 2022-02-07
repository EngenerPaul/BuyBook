from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


# Authentication
# AuthenticationForm needed for using authentication 
class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

# Registration
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
