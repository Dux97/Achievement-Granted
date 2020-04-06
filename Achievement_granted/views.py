import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from games.forms import SendUrlForm
from bs4 import BeautifulSoup


def home(request):
    return render(request, 'pages/home.html', {})


@login_required(login_url='/account/steam/login')
def games(request):
    return render(request, 'pages/games.html', {})


@login_required(login_url='/account/steam/login')
def achievement(request):
    if request.method == 'POST':
        form = SendUrlForm(request.POST)
        if form.is_valid():
            url = request.POST['url']

            response = requests.get(url).text

            bf_content = BeautifulSoup(response, "html.parser")

            table = bf_content.find('table', attrs={'class': 'wikitable'})
            rows = table.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            print(data)
            return render(request, 'pages/achievement.html/', {'value': data})
    else:
        form = SendUrlForm()
    return render(request, 'pages/achievement.html', {'form': form})


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})

  
def guide(request):
    return  render(request, 'pages/guide.html', {})
