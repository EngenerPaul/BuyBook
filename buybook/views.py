from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Book, Author, Genre
from .forms import AuthUserForm, RegisterUserForm, CommentForm

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

class BookDetail(DetailView, FormMixin):
    model = Book
    template_name = 'buybook/bookdetail.html'
    context_object_name = 'book'

    form_class = CommentForm

    # needed for rezeive information from form (form_class = CommentForm)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)
      
    # needed for save and update (set user_id and book_id) form
    def form_valid(self, request, form):
        self.object = form.save(commit=False)
        self.object.user_id = request.user.pk  # create foreign key user in CommentForm
        self.object.book = self.get_object()  # create foreign key book in CommentForm
        self.object.save()
        return super().form_valid(form)
    
    # needed for post and get_context_data functions to work correctly
    def form_invalid(self, form):
        self.object = self.get_object() 
        return super().form_invalid(form)

    # needed for refresh the page after saving the form
    def get_success_url(self, **kwargs):
        return reverse_lazy('book_detail', kwargs={'slug': self.get_object().slug})

    # needed for display list of comments
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_comments'] = self.object.comments.all()  # comments is a foreign key (related_name) of Comment model 
        return context


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
