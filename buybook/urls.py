from django.contrib import admin
from django.urls import path, include

from .views import Home, BookDetail, BookByGenre, \
                   CustomLoginView, CustomRegistration, CustomLogOut, \
                   BasketView, CreateBasketBook, Move_to_Marked_Button, Delete_from_basket_Button, \
                   MarkedView, CreateMarkedBook, Move_to_Basket_Button, Delete_from_marked_Button

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('bookdetail/<str:slug>', BookDetail.as_view(), name='book_detail_page'),
    path('genre/<str:slug>', BookByGenre.as_view(), name='genre_page'),

    path('login', CustomLoginView.as_view(), name='login_page'),
    path('registration', CustomRegistration.as_view(), name='registration_page'),
    path('logout', CustomLogOut.as_view(), name='logout_page'),
   
    path('basket', BasketView.as_view(), name='basket_url'),
    path('basket/add/<int:pk>', CreateBasketBook.as_view(), name='add_to_basket'),
    path('basket/from_basket_to_marked/<int:pk>', Move_to_Marked_Button.as_view(), name='move_to_marked'),
    path('basket/delete/<int:pk>', Delete_from_basket_Button.as_view(), name='delete_basket'),

    path('marked', MarkedView.as_view(), name='marked_url'),
    path('marked/add/<int:pk>', CreateMarkedBook.as_view(), name='add_to_marked'),
    path('marked/from_marked_to_basket/<int:pk>', Move_to_Basket_Button.as_view(), name='move_to_basket'),
    path('marked/delete/<int:pk>', Delete_from_marked_Button.as_view(), name='delete_marked'),

]
