from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from games.forms import SendUrlForm


def home(request):
    return render(request, 'pages/home.html', {})


def games(request):
    return render(request, 'pages/games.html', {})


def achievement(request):
    if request.method == 'POST':
        form = SendUrlForm(request.POST)
        if form.is_valid():
            value = "przesłano"
            return render(request, 'pages/achievement.html/',{'value': value})
    else:
        form = SendUrlForm()
    return render(request, 'pages/achievement.html', {'form': form})


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})
