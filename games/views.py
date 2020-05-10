from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
        data = {"games": resp["response"],
                'errorDescription': request.session.get('noAchievements')}
        try:
            del request.session['noAchievements']
        except KeyError:
            pass
    except (ConnectionError, Timeout):
        data = {'errorDescription': "Something wrong. Please try again."}
    return render(request, 'pages/games.html', data)


@login_required(login_url='/account/steam/login')
def achievement(request, appid):
    errorDescr = {"errorDescription": False}
    if request.method != 'POST':
        form = SendUrlForm()
        try:
            game = getGameInfo(appid)
            unlockedAchievement = getUnlockedAchievment(request, appid)
            try:
                steamAchievements = game['game']['availableGameStats']['achievements']
            except KeyError:
                errorDescr = {"errorDescription": "No achievements in this game."}
                request.session['noAchievements'] = errorDescr
                return redirect('games')
            try:
                playerUnlocked = [achievement['name'] for achievement in
                                  unlockedAchievement['playerstats']['achievements']]
            except KeyError:
                playerUnlocked = []
        except (ConnectionError, Timeout):
            errorDescr = {'errorDescription': "Something wrong. Please try again."}
        try:
            fullAchievementList = addUnlockedToDetails(steamAchievements, playerUnlocked)
            request.session[f'fullAchievementList{appid}'] = fullAchievementList
            request.session[f'selected_project_id{appid}'] = steamAchievements
        except UnboundLocalError:
            errorDescr = {"errorDescription": "No achievements in this game."}
            fullAchievementList = {}
        data = {'achievementSteam': fullAchievementList,
                "error": errorDescr, 'form': form}
    else:
        form = SendUrlForm(request.POST)
        if form.is_valid():
            url = request.POST['url']
            fullAchievementList = request.session.get(f'fullAchievementList{appid}')
            data = {'achievementSteam': scrapLinkAndAddToTable(url, fullAchievementList),
                "error": errorDescr, 'form': form}
    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})
