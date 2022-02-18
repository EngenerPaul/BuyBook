from datetime import datetime, timedelta

# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q

from .models import Book, Author, Genre, Comment, Basket, Marked, Order, OrderDetails
from .forms import AuthUserForm, RegisterUserForm, CommentForm, BasketForm, OrderForm



class Home(ListView):
    """Show a list of books on the main page"""

    model = Book
    template_name = 'buybook/index.html'
    context_object_name = 'book_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all() # Show list of genres
        context['buy_url'] = 'add_to_basket'  # url-adress for button "buy"
        context['mark_url'] = 'add_to_marked'  # url-adress for button "mark"
        return context


class BookDetail(DetailView, FormMixin):
    """Show details of the book"""

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
        return reverse_lazy('book_detail_page', kwargs={'slug': self.get_object().slug})

    # needed for display list of comments
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_comments'] = self.object.comments.all()  # comments is a foreign key (related_name) of Comment model 
        context['buy_url'] = 'add_to_basket_from_detail'  # url-adress for button "buy"
        context['mark_url'] = 'add_to_marked_from_detail'  # url-adress for button "mark"
        return context


class DeleteComment(DeleteView):
    """This button removes the comment in the book details"""

    model = Comment
    template_name = 'buybook/bookdetail.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('book_detail_page', kwargs={'slug': self.get_object().book.slug})


class BookByGenre(ListView):
    """Show books by genres"""

    template_name = 'buybook/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return Book.objects.filter(genre__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Genre.objects.get(slug=self.kwargs['slug'])
        context['genres'] = Genre.objects.all()
        context['buy_url'] = 'add_to_basket'  # url-adress for button "buy"
        context['mark_url'] = 'add_to_marked'  # url-adress for button "mark"
        return context


class Search(ListView):
    """Search books by title and author"""

    template_name = 'buybook/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        # view_variable take from template form: <input name="view_variable"...>
        queryset = Book.objects.filter(
            Q(title__icontains=self.request.GET.get('view_variable')) |
            Q(author__full_name__icontains=self.request.GET.get('view_variable'))
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context


class OrderCreateView(CreateView):
    """Show the page for creating a new order"""

    model = Order
    template_name = 'buybook/order_creation.html'

    form_class = OrderForm
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)
        

    def form_valid(self, request, form):
        self.object = form.save(commit=False)
        self.object.user_id = request.user
        self.object.total_cost = int(request.POST['total_cost'])
        self.object.save()

        # enumerate books in basket...
        for basket_book in Basket.objects.filter(user_id=request.user):

            """ A ManyToMany field is filled after create new object (in both models).
            Futher we create list objects from another model - Basket.objects.filter(...).
            Note: our model (Order) tied with Book model, because we use FpreignKey - book_id.
            We scroll through Book objects 
            and use the method add() to the ManyToMany field - self.object.book_id
            Documentation: https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/"""

            self.object.book_id.add(basket_book.book_id) # we add the Book object!

            """For saving quantities books and their cost we must create and fill 
            additional table - OrderDetails"""
        
            OrderDetails.objects.create(
                order_id= self.object,
                book_id= basket_book.book_id,
                quantity= basket_book.quantity,
                cost= basket_book.book_id.cost,
            )
        
            """Additionally change quantity of books in stock"""

            book = basket_book.book_id
            book.units_in_stock -= basket_book.quantity
            book.save()

        # presently we need to clear the Basket table
        Basket.objects.filter(user_id=request.user).delete()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['products'] = Basket.objects.filter(user_id=self.request.user)
        context['quantity'] = 0
        context['cost'] = 0
        context['date'] = datetime.now().date() + timedelta(days=14)
        if self.request.user.is_authenticated:
            for obj in Basket.objects.filter(user_id=self.request.user):
                context['quantity'] += obj.quantity
                context['cost'] += obj.book_id.cost * obj.quantity
        return context



########################################################################
#####     Authentication, Registration, LogOut and Profile         #####
########################################################################

class CustomLoginView(LoginView):
    """Authentication"""

    template_name = "buybook/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    # because success_url variable does't work
    def get_success_url(self):
        return self.success_url

class CustomRegistration(CreateView):
    """Registration"""

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
    """LogOut"""

    next_page = reverse_lazy('home')

class Profile(DetailView):
    """User profile"""

    model = User
    template_name = 'buybook/profile.html'
    context_object_name = 'user'

    def get_context_data(self, *args, **kwarg):
        context = super().get_context_data(*args, **kwarg)
        context['orders'] = Order.objects.filter(user_id=self.request.user)
        return context


########################################################################
#####    Basket and marked page views as well as their buttons:    #####
#####  Purchase and mark buttons from homepage, basket and marked  #####
########################################################################

# button Купить - create new record in the Basket
class CreateBasketBook(View):
    """The button for purchase on homepage"""

    # the form method in buttons.html is "post"
    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Basket.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Basket.objects.create(book_id=book_obj, user_id=user_obj)
            # If the object exists then nothing happens
        return redirect('home')

class CreateBasketBook_BDP(View):
    """The button for purchase in book detail page (BDP)"""

    # the form method in buttons.html is "post"
    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Basket.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Basket.objects.create(book_id=book_obj, user_id=user_obj)
            # If the object exists then nothing happens
        return redirect('book_detail_page', slug=book_obj.slug)

# List of book in basket
class BasketView(ListView):
    """Display list of book in the basket-page"""

    template_name = 'buybook/basket.html'
    context_object_name = 'basket_books'
    form_class = BasketForm
    success_url = reverse_lazy('basket')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Basket.objects.filter(user_id=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity'] = 0
        context['cost'] = 0
        if self.request.user.is_authenticated:
            for obj in Basket.objects.filter(user_id=self.request.user):
                context['quantity'] += obj.quantity
                context['cost'] += obj.book_id.cost * obj.quantity
        return context

class ChangeQuantity(View):
    """This class changes quantity books in the basket"""

    def post(self, request, pk, *args, **kwargs):
        obj_basket_record = Basket.objects.get(pk=pk)
        new_value = int(request.POST[str(pk)])
        max_value = Basket.objects.get(pk=pk).book_id.units_in_stock
        
        if new_value > max_value:
            obj_basket_record.quantity = max_value
        elif new_value > 0:
            obj_basket_record.quantity = new_value  
        
        obj_basket_record.save()
        return redirect('basket_page')

class Move_to_Marked_Button(View):
    """This button move book from basket list to marked list"""

    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Marked.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Marked.objects.create(book_id=book_obj, user_id=user_obj)
        Basket.objects.get(book_id=book_obj, user_id=user_obj).delete()
        return redirect('basket_page')

class Delete_from_basket_Button(View):
    """This button delete book from basket list"""

    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        Basket.objects.get(book_id=book_obj, user_id=user_obj).delete()
        return redirect('basket_page')



# button Купить - create new record in the Basket
class CreateMarkedBook(View):
    """The button for marking on homepage"""

    # the form method in buttons.html is "post"
    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Marked.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Marked.objects.create(book_id=book_obj, user_id=user_obj)
            # If the object exists then nothing happens
        return redirect('home')

class CreateMarkedBook_BDP(View):
    """The button for marking in book detail page (BDP)"""

    # the form method in buttons.html is "post"
    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Marked.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Marked.objects.create(book_id=book_obj, user_id=user_obj)
            # If the object exists then nothing happens
        return redirect('book_detail_page', slug=book_obj.slug)

# List of book in basket
class MarkedView(ListView):
    """Display list of book in the marked-page"""

    template_name = 'buybook/marked.html'
    context_object_name = 'marked_books'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Marked.objects.filter(user_id=self.request.user)

class Move_to_Basket_Button(View):
    """This button move book from marked list to basket list"""

    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        if not Basket.objects.filter(book_id=book_obj, user_id=user_obj).exists():
            Basket.objects.create(book_id=book_obj, user_id=user_obj)
        Marked.objects.get(book_id=book_obj, user_id=user_obj).delete()
        return redirect('marked_page')

class Delete_from_marked_Button(View):
    """This button delete book from marked list"""

    def post(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.get(pk=pk)
        user_obj = request.user
        Marked.objects.get(book_id=book_obj, user_id=user_obj).delete()
        return redirect('marked_page')

