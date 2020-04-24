import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from games.forms import SendUrlForm


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
            results=scrapTableFromUrl(url)
            

            return render(request, 'pages/achievement.html/', {'value': results})
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


def scrapTableFromUrl(url):
    response = requests.get(url).text

    bf_content = BeautifulSoup(response, "html.parser")

    table = bf_content.find('table', attrs={'class': 'wikitable'})
    # rows = table.find_all('tr')
    #
    # data = []
    # for row in rows:
    #     cols = row.find_all('td')
    #     cols = [ele.text.strip() for ele in cols]
    #     data.append([ele for ele in cols if ele])

    headers = [header.text.strip("\n") for header in table.find_all('th')]

    # results = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
    #            for row in table.find_all('tr')]
    results=[]
    for b,row in enumerate(table.find_all('tr')):
        ro={}
        for i, cell in enumerate(row.find_all('td')):
            if headers[i]=="Name":
                ro['link']=cell

            ro[headers[i]]=cell.text
        results.append(ro)

    results.pop(0)



    print(results)
    return results
