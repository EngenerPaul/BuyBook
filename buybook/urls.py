from django.contrib import admin
from django.urls import path, include

from .views import first_func

urlpatterns = [
    path('', first_func),
]
