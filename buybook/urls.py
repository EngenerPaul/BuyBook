from django.contrib import admin
from django.urls import path, include

from .views import Home, CustomLoginView, CustomRegistration

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('registration', CustomRegistration.as_view(), name='registration')
]
