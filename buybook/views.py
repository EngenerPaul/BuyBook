from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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

class BookDetail(DetailView):
    model = Book
    template_name = 'buybook/bookdetail.html'
    context_object_name = 'book'

    def get_succes_url(self):
        return reverse_lazy('book_detail', kwargs={'slug': self.get_object.slug})

# Authentication
class CustomLoginView(LoginView):
    template_name = "buybook/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    # because success_url variable does't work
    def get_success_url(self):
        return self.success_url

# Registration
class CustomRegistration(CreateView):
    model = User
    template_name = 'buybook/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """the method is overridden
        added auto-authentication"""

        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid

class CustomLogOut(LogoutView):
    next_page = reverse_lazy('home')
