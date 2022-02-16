from django.contrib import admin
from django.urls import path, include

from .views import Home, BookDetail, BookByGenre, Search, \
                   CustomLoginView, CustomRegistration, CustomLogOut, \
                   BasketView, CreateBasketBook, CreateBasketBook_BDP, \
                       Move_to_Marked_Button, Delete_from_basket_Button, ChangeQuantity, \
                   MarkedView, CreateMarkedBook, CreateMarkedBook_BDP, \
                       Move_to_Basket_Button, Delete_from_marked_Button\
                   

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('bookdetail/<str:slug>', BookDetail.as_view(), name='book_detail_page'),
    path('genre/<str:slug>', BookByGenre.as_view(), name='genre_page'),
    path('search', Search.as_view(), name='search'),

    path('login', CustomLoginView.as_view(), name='login_page'),
    path('registration', CustomRegistration.as_view(), name='registration_page'),
    path('logout', CustomLogOut.as_view(), name='logout_page'),
   
    path('basket', BasketView.as_view(), name='basket_page'),  # adress basket-of page
    path('basket/add/<int:pk>', CreateBasketBook.as_view(), name='add_to_basket'),  # adress button in index.html
    path('basket/add_DBP/<int:pk>', CreateBasketBook_BDP.as_view(), name='add_to_basket_from_detail'),  # adress same button in bookdetail.html
    path('basket/from_basket_to_marked/<int:pk>', Move_to_Marked_Button.as_view(), name='move_to_marked'),  # adress marked button in basket
    path('basket/delete/<int:pk>', Delete_from_basket_Button.as_view(), name='delete_basket'),  # adress delete button in basket
    path('basket/change-quantity/<int:pk>', ChangeQuantity.as_view(), name='change_quantity_url'),  # adress button for change quantity in basket

    path('marked', MarkedView.as_view(), name='marked_page'),  # adress of marked-page
    path('marked/add/<int:pk>', CreateMarkedBook.as_view(), name='add_to_marked'),  # adress button in index.html
    path('marked/add_DBP/<int:pk>', CreateMarkedBook_BDP.as_view(), name='add_to_marked_from_detail'),  # adress same button in bookdetail.html
    path('marked/from_marked_to_basket/<int:pk>', Move_to_Basket_Button.as_view(), name='move_to_basket'),  # adress buy button in marked
    path('marked/delete/<int:pk>', Delete_from_marked_Button.as_view(), name='delete_marked'),  # adress delete button in marked

]
