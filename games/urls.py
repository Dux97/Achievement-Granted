from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home),
    path('games/', views.games, name='games'),
    path('games/<int:appid>/achievement/', views.achievement, name='achievement'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('error404', views.error404, name='error404'),
    path('account/', include('allauth.urls')),
    path('guide/', views.guide, name='guide'),
]
