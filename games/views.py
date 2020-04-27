from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import ConnectionError, Timeout

from games.forms import SendUrlForm
from games.utils import scrapTableFromUrl, getUserGames, getGameInfo, getUnlockedAchievment, \
    addUnlockedToDetails, addWikiLink


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
        if form.is_valid():
            url = request.POST['url']
            try:
                gameScrapped = scrapTableFromUrl(url)
                game = getGameInfo(appid)
                unlockedAchievement = getUnlockedAchievment(request, appid)
                try:
                    steamAchievements = game['game']['availableGameStats']['achievements']
                except KeyError:
                    data = {"errorDescription": "No achievements in this game."}
                else:
                    steamAchievements = game['game']['availableGameStats']['achievements']
                    # gameAchievements = addWikiLink(steamAchievements, gameScrapped)
                try:
                    playerUnlocked = [achievement['name'] for achievement in
                                      unlockedAchievement['playerstats']['achievements']]
                except KeyError:
                    playerUnlocked = []
            except (ConnectionError, Timeout):
                data = {'errorDescription': "Something wrong. Please try again."}
            try:
                data
            except UnboundLocalError:
                data = {'achievementSteam': addUnlockedToDetails(steamAchievements, playerUnlocked),
                        'achievementScrap': gameScrapped}
    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})
