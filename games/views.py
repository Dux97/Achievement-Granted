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


    headers = [header.text.strip("\n") for header in table.find_all('th')]


    results=[]
    #url2=url[:url.rfind('/')]
    spliturl = url.rsplit('/wiki', 1)[0]

    for b,row in enumerate(table.find_all('tr')):
        fullrow={}
        for i, cell in enumerate(row.find_all('td')):
            if headers[i]=="Name":
                if(cell.find('a').get('href')):
                    fullrow['link']=spliturl+cell.find('a').get('href')

                else:
                    fullrow['link'] =spliturl+"#"
            fullrow[headers[i]]=cell.text.strip("\n")
        results.append(fullrow)


    results.pop(0)

    return results
