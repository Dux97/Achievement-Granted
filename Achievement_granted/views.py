from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html', {})


def games(request):
    return render(request, 'pages/games.html', {})


def achievement(request):
    return render(request, 'pages/achievement.html', {})


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})