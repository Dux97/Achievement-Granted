from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('new', views.url_new, name='url_new')
]