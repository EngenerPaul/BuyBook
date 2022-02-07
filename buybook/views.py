from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from .models import Book, Author, Genre
from .forms import AuthUserForm, RegisterUserForm

def first_func(request):
    template_name = 'buybook/index.html'
    content = {
        'hello' : 'hello world'
    }
    return render(request, template_name, content)

class Home(ListView):
    model = Book
    template_name = 'buybook/index.html'
    context_object_name = 'all_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context


# Authentication
class CustomLoginView(LoginView):
    template_name = "buybook/login.html"
    from_class = AuthUserForm
    success_url = reverse_lazy('home')

# Registration
class CustomRegistration(CreateView):
    model = User
    template_name = 'buybook/registration.html'
    from_class = RegisterUserForm
    success_url = reverse_lazy('home')