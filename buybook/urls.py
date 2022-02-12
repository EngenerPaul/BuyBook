from unicodedata import name
from django.contrib import admin
from django.urls import path, include

from .views import Home, BookDetail, CustomLoginView, CustomRegistration, \
                   CustomLogOut

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('bookdetail/<str:slug>', BookDetail.as_view(), name='book_detail'),
    path('login', CustomLoginView.as_view(), name='login_page'),
    path('registration', CustomRegistration.as_view(), name='registration_page'),
    path('logout', CustomLogOut.as_view(), name='logout_page'),
    
]
