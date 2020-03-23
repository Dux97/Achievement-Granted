from django import forms

from .models import Game


class UrlForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'wiki_url',)


class SendUrlForm(forms.form):
    url = forms.CharField(max_length=30)
