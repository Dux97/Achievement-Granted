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
    return render(request, 'pages/games.html', {"games": data["response"]})


@login_required(login_url='/account/steam/login')
def achievement(request, appid):
    if request.method != 'POST':
        form = SendUrlForm()
        data = {'form': form}
    else:
        form = SendUrlForm(request.POST)
        if form.is_valid():
            url = request.POST['url']
            gameScrapped = scrapTableFromUrl(url)

            api_base = "http://api.steampowered.com/"
            method = "ISteamUserStats/GetSchemaForGame/v2/"
            params = {"key": env("STEAM_KEY"), "appid": appid, "format": "json"}
            resp = requests.get(api_base + method, params)
            game = resp.json()

            method = "ISteamUserStats/GetUserStatsForGame/v0002/"
            for account in SocialAccount.objects.filter(user=request.user):
                provider_account = account.get_provider_account().account.extra_data
            params = {"key": env("STEAM_KEY"), "appid": appid, "steamid": provider_account["steamid"], "format": "json"}
            resp = requests.get(api_base + method, params)
            unlockedAchievement = resp.json()
            playerUnlocked = [achievement['name'] for achievement in unlockedAchievement['playerstats']['achievements']]
            gameAchievements = game['game']['availableGameStats']['achievements']
            for achievement in gameAchievements:
                if achievement['name'] in playerUnlocked:
                    achievement['achieved'] = 1
                else:
                    achievement['achieved'] = 0
            data = {'achievementSteam': gameAchievements, 'achievementScrap': gameScrapped}

    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})


def scrapTableFromUrl(url):
    response = requests.get(url).text
    bf_content = BeautifulSoup(response, "html.parser")
    table = bf_content.find('table', attrs={'class': 'wikitable'})
    headers = [header.text.strip("\n") for header in table.find_all('th')]
    results = []
    splitUrl = url.rsplit('wiki', 1)[0]
    for b, row in enumerate(table.find_all('tr')):
        fullRow = {}
        for i, cell in enumerate(row.find_all('td')):
            if headers[i] == "Name":
                if cell.find('a').get('href'):
                    fullRow['link'] = splitUrl + cell.find('a').get('href')
                else:
                    fullRow['link'] = "brak linku"
            fullRow[headers[i]] = cell.text.strip("\n")
        results.append(fullRow)
    results.pop(0)
    return results
