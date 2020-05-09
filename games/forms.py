from django import forms

from .models import Game


class UrlForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'wiki_url',)


class SendUrlForm(forms.Form):
    url = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Url',
                                                                                  }))
