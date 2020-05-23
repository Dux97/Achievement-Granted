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


def scrapLinkAndAddToTable(url, table):
    response = requests.get(url).text
    bf_content = BeautifulSoup(response, "html.parser")
    domain = url.split("//")[-1].split("/")[0]
    for row in table:
        if row["displayName"][-1] == " ":
            row["displayName"] = row["displayName"][:-1]
        if bf_content.find("a", text=row["displayName"]):
            row["link"] = "https://" + domain + bf_content.find("a", text=row["displayName"]).get("href")
        else:
            row["link"] = "#"
    return table


def countLinks(url, table):
    counter = 0
    response = requests.get(url).text
    bf_content = BeautifulSoup(response, "html.parser")
    domain = url.split("//")[-1].split("/")[0]
    for row in table:
        if row["displayName"][-1] == " ":
            row["displayName"] = row["displayName"][:-1]
        if bf_content.find("a", text=row["displayName"]):
            counter += 1
    return counter
