from django import forms
from django.forms import ModelForm

from .models import Game


class UrlForm(ModelForm):
    link = forms.CharField(label="", max_length=150,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Url',
                                       'type': 'text',
                                       'list': 'linkList',
                                      'class': "form-control",
                               }))

    class Meta:
        model = Game
        fields = ['link']
