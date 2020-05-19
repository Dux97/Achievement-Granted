from django.contrib import admin
from django.urls import path, include
from games import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
]
handler404 = views.error404
