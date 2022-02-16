from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Basket


# Authentication
# AuthenticationForm needed for using authentication 
class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        
        # labels = {...}  doesn't work!
        # widgets = {...}  doesn't work!
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Укажите Ваше имя'
            self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

# Registration
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Имя пользователя', 
            'password': 'Пароль',
        }
        widgets = {
            'username':forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Укажите Ваше имя'
            }),
            'password':forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите пароль'
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'estimate', )
        labels = {
            'text': 'Оставьте свой комментарий',
            'estimate': 'Ваша оценка',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш комментарий...'
            }),
            'estimate': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 200px',
            })
        }

class BasketForm(forms.ModelForm):
    class Meta: 
        model = Basket
        fields = ('quantity', )