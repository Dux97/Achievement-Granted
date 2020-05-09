from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import ConnectionError, Timeout

from games.forms import SendUrlForm
from games.utils import getUserGames, getGameInfo, getUnlockedAchievment, \
    addUnlockedToDetails, scrapLinkAndAddToTable


def home(request):
    return render(request, 'pages/home.html', {})


@login_required(login_url='/account/steam/login')
def games(request):
    try:
        resp = getUserGames(request)
        data = {"games": resp["response"]}
    except (ConnectionError, Timeout):
        data = {'errorDescription': "Something wrong. Please try again."}
    return render(request, 'pages/games.html', data)


@login_required(login_url='/account/steam/login')
def achievement(request, appid):
    if request.method != 'POST':
        form = SendUrlForm()
        data = {'form': form}
    else:
        form = SendUrlForm(request.POST)
        errorDescr = {"errorDescription": False}
        if form.is_valid():
            url = request.POST['url']
            try:
                game = getGameInfo(appid)
                unlockedAchievement = getUnlockedAchievment(request, appid)
                try:
                    steamAchievements = game['game']['availableGameStats']['achievements']
                    scrapedAchievements = scrapLinkAndAddToTable(url, steamAchievements)
                except KeyError:
                    errorDescr = {"errorDescription": "No achievements in this game."}
                try:
                    playerUnlocked = [achievement['name'] for achievement in
                                      unlockedAchievement['playerstats']['achievements']]
                except KeyError:
                    playerUnlocked = []
            except (ConnectionError, Timeout):
                errorDescr = {'errorDescription': "Something wrong. Please try again."}
            data = {'achievementSteam': addUnlockedToDetails(scrapedAchievements, playerUnlocked),
                    "error": errorDescr}
    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})
