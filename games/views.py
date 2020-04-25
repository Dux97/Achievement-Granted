from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import ConnectionError, Timeout
from games.forms import SendUrlForm
from games.utils import scrapTableFromUrl, getUserGames, getGameInfo, getUnlockedAchievment, \
    addUnlockedToDetails


def home(request):
    return render(request, 'pages/home.html', {})


@login_required(login_url='/account/steam/login')
def games(request):
    data = getUserGames(request)
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
            try:
                gameScrapped = scrapTableFromUrl(url)
                game = getGameInfo(appid)
                unlockedAchievement = getUnlockedAchievment(request, appid)
                gameAchievements = game['game']['availableGameStats']['achievements']
                if not unlockedAchievement:
                    playerUnlocked = ["nothingUnlocked"]
                else:
                    playerUnlocked = [achievement['name'] for achievement in
                                      unlockedAchievement['playerstats']['achievements']]

                data = {'achievementSteam': addUnlockedToDetails(gameAchievements, playerUnlocked),
                        'achievementScrap': gameScrapped}
            except (ConnectionError, Timeout):
                data = {'error': "Something wrong. Please try again."}

    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})



