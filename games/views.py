import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from games.forms import SendUrlForm
from allauth.socialaccount.models import SocialAccount
import environ


env = environ.Env()
env.read_env(env.str('ENV_PATH', '.env'))

def home(request):
    return render(request, 'pages/home.html', {})


@login_required(login_url='/account/steam/login')
def games(request):
    for account in SocialAccount.objects.filter(user=request.user):
        provider_account = account.get_provider_account().account.extra_data
    api_base = "http://api.steampowered.com/"
    method = "IPlayerService/GetOwnedGames/v0001/"
    params = {"key": env("STEAM_KEY"), "steamid": provider_account["steamid"], "format":"json", "include_appinfo":"1"}
    resp = requests.get(api_base + method, params)
    data = resp.json()
    method = "ISteamUserStats/GetSchemaForGame/v2/"
    games = data["response"]["games"]
    gameList = {}
    for game in games:
        params = {"key": env("STEAM_KEY"), "appid": game["appid"], "format": "json"}
        resp = requests.get(api_base + method, params)
        data = resp.json()
        gameList[game["appid"]] = data["game"]
    return render(request, 'pages/games.html', {"games": data["response"]})


@login_required(login_url='/account/steam/login')
def achievement(request, appid):
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
    return render(request, 'pages/guide.html', {})
