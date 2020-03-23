from django.shortcuts import render
from .forms import UrlForm


# Create your views here.
def url_new(request):
    form = UrlForm()
    return render(request, 'pages/test.html', {'form': form})
