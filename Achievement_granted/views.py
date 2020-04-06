from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html', {})


@login_required(login_url='/account/steam/login')
def games(request):
    return render(request, 'pages/games.html', {})


@login_required(login_url='/account/steam/login')
def achievement(request):
    return render(request, 'pages/achievement.html', {})


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return  render(request, 'pages/guide.html', {})

