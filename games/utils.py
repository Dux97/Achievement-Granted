import environ
import requests
from allauth.socialaccount.models import SocialAccount
from bs4 import BeautifulSoup

env = environ.Env()
env.read_env(env.str('ENV_PATH', '.env'))
api_base = "http://api.steampowered.com/"


def getProfileID(request):
    for account in SocialAccount.objects.filter(user=request.user):
        provider_account = account.get_provider_account().account.extra_data
        return provider_account["steamid"]


def getUserGames(request):
    method = "IPlayerService/GetOwnedGames/v0001/"
    params = {"key": env("STEAM_KEY"), "steamid": getProfileID(request), "format": "json", "include_appinfo": "1"}
    resp = requests.get(api_base + method, params)
    return resp.json()


def getGameInfo(appid):
    method = "ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": env("STEAM_KEY"), "appid": appid, "format": "json"}
    resp = requests.get(api_base + method, params)
    return resp.json()


def getUnlockedAchievment(request, appid):
    method = "ISteamUserStats/GetUserStatsForGame/v0002/"
    params = {"key": env("STEAM_KEY"), "appid": appid, "steamid": getProfileID(request), "format": "json"}
    resp = requests.get(api_base + method, params)
    return resp.json()


def addUnlockedToDetails(gameAchievements, playerUnlocked):
    for achievement in gameAchievements:
        if achievement['name'] in playerUnlocked:
            achievement['achieved'] = 1
        else:
            achievement['achieved'] = 0
    return gameAchievements


def scrapTableFromUrl(url):
    response = requests.get(url).text
    bf_content = BeautifulSoup(response, "html.parser")
    table = bf_content.find('table', attrs={'class': 'wikitable'})
    headers = [header.text.strip("\n") for header in table.find_all('th')]
    results = []
    splitUrl = url.rsplit('wiki', 1)[0]
    for row in table.find_all('tr'):
        fullRow = {}
        for cellIndex, cell in enumerate(row.find_all('td')):
            if headers[cellIndex] == "Name":
                if cell.find('a').get('href'):
                    fullRow['link'] = splitUrl + cell.find('a').get('href')
                else:
                    fullRow['link'] = "#"
            fullRow[headers[cellIndex]] = cell.text.strip("\n")
        results.append(fullRow)
    results.pop(0)
    return results
