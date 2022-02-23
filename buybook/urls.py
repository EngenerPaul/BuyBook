from django.contrib import admin
from django.urls import path, include

from .views import Home, BookDetail, DeleteComment, BookByGenre, Search, \
                   OrderCreateView, \
                   CustomLoginView, CustomRegistration, CustomLogOut, Profile,\
                   BasketView, CreateBasketBook, CreateBasketBook_BDP, \
                   Move_to_Marked_Button, Delete_from_basket_Button, \
                   ChangeQuantity, \
                   MarkedView, CreateMarkedBook, CreateMarkedBook_BDP, \
                   Move_to_Basket_Button, Delete_from_marked_Button

urlpatterns = [
    path('', Home.as_view(),
         name='home'),
    path('bookdetail/<str:slug>', BookDetail.as_view(),
         name='book_detail_page'),
    path('bookdetail/delete_comment/<int:pk>', DeleteComment.as_view(),
         name='delete_comment_url'),
    path('genre/<str:slug>', BookByGenre.as_view(),
         name='genre_page'),
    path('search', Search.as_view(),
         name='search'),
    path('order', OrderCreateView.as_view(),
         name='create_order_page'),

    path('login', CustomLoginView.as_view(),
         name='login_page'),
    path('registration', CustomRegistration.as_view(),
         name='registration_page'),
    path('logout', CustomLogOut.as_view(),
         name='logout_page'),
    path('profile/id=<int:pk>', Profile.as_view(),
         name='profile'),

    path('basket', BasketView.as_view(),
         name='basket_page'),  # adress basket-of page
    path('basket/add/<int:pk>', CreateBasketBook.as_view(),
         name='add_to_basket'),  # adress button in index.html
    # adress same button in bookdetail.html
    path('basket/add_DBP/<int:pk>', CreateBasketBook_BDP.as_view(),
         name='add_to_basket_from_detail'),
    # adress marked button in basket
    path('basket/from_basket_to_marked/<int:pk>',
         Move_to_Marked_Button.as_view(), name='move_to_marked'),
    path('basket/delete/<int:pk>', Delete_from_basket_Button.as_view(),
         name='delete_basket'),  # adress delete button in basket
    # adress button for change quantity in basket
    path('basket/change-quantity/<int:pk>', ChangeQuantity.as_view(),
         name='change_quantity_url'),

    path('marked', MarkedView.as_view(),
         name='marked_page'),  # adress of marked-page
    path('marked/add/<int:pk>', CreateMarkedBook.as_view(),
         name='add_to_marked'),  # adress button in index.html
    # adress same button in bookdetail.html
    path('marked/add_DBP/<int:pk>', CreateMarkedBook_BDP.as_view(),
         name='add_to_marked_from_detail'),
    # adress buy button in marked
    path('marked/from_marked_to_basket/<int:pk>',
         Move_to_Basket_Button.as_view(), name='move_to_basket'),
    path('marked/delete/<int:pk>', Delete_from_marked_Button.as_view(),
         name='delete_marked'),  # adress delete button in marked

]
