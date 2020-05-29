from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import ConnectionError, Timeout
from requests.exceptions import MissingSchema

from games.forms import UrlForm
from games.models import Game
from games.utils import getUserGames, getGameInfo, getUnlockedAchievment, \
    addUnlockedToDetails, scrapLinkAndAddToTable, isLinkEfficiency


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
    errorDescr = {"errorDescription": []}
    linksDB = Game.objects.filter(name=appid)
    if request.method != 'POST':
        form = UrlForm()
        try:
            game = getGameInfo(appid)
            unlockedAchievement = getUnlockedAchievment(request, appid)
            try:
                steamAchievements = game['game']['availableGameStats']['achievements']
            except KeyError:
                request.session['noAchievements'] = {"errorDescription": "No achievements in this game."}
                return redirect('games')
            try:
                playerUnlocked = [achievement['name'] for achievement in
                                  unlockedAchievement['playerstats']['achievements']]
            except KeyError:
                playerUnlocked = []
        except (ConnectionError, Timeout, JSONDecodeError):
            if JSONDecodeError:
                return redirect('guide')
            else:
                errorDescr['errorDescription'].append("Something wrong. Please try again.")
        try:
            fullAchievementList = addUnlockedToDetails(steamAchievements, playerUnlocked)
            request.session[f'fullAchievementList{appid}'] = fullAchievementList
            request.session[f'selected_project_id{appid}'] = steamAchievements
        except UnboundLocalError:
            errorDescr['errorDescription'].append("No achievements in this game.")
            fullAchievementList = {}
        data = {'achievementSteam': fullAchievementList,
                "error": errorDescr, 'form': form, 'links': linksDB }
    else:
        form = UrlForm(request.POST)
        url = request.POST['link']
        fullAchievementList = request.session.get(f'fullAchievementList{appid}')
        try:
            scrapedTable, counterEfficiency = scrapLinkAndAddToTable(url, fullAchievementList)
            data = {'achievementSteam': scrapedTable,
                    "error": errorDescr, 'form': form, 'links': linksDB}
            try:
                if isLinkEfficiency(counterEfficiency, fullAchievementList):
                    instance = form.save(commit=False)
                    instance.name = appid
                    instance.save()
            except ValueError:
                pass
        except (MissingSchema, ConnectionError):
            errorDescr['errorDescription'].append("Bad url for scrap. Try diffrent.")
            data = {'achievementSteam': fullAchievementList,
                    "error": errorDescr, 'form': form, 'links': linksDB}
    return render(request, 'pages/achievement.html', data)


def about(request):
    return render(request, 'pages/about.html', {})


def base(request):
    return render(request, 'base.html', {})


def error404(request, exception=None):
    return render(request, '404.html', {})


def guide(request):
    return render(request, 'pages/guide.html', {})
