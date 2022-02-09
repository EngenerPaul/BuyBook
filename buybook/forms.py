from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


# Authentication
# AuthenticationForm needed for using authentication 
class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        
        # doesn't work!
        # labels = {
        #     'username': 'Name', 
        #     'password': 'Password',
        # }
        # widgets = {
        #     'username':forms.TextInput(attrs={
        #         'class': 'form-control', 
        #         'placeholder': 'Please enter your name'
        #     }),
        #     'password':forms.TextInput(attrs={
        #         'class': 'form-control', 
        #         'placeholder': 'Please enter your password'
        #     })
        # }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# Registration
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Name', 
            'password': 'Password',
        }
        widgets = {
            'username':forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Please enter your name'
            }),
            'password':forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Please enter your password'
            })
        }
    
    # needed for saving password
    # .\venv\Lib\site-packages\django\contrib\auth\forms.py - class UserCreationForm
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
