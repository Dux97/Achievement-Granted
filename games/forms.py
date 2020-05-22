from django import forms
from django.forms import ModelForm
from .models import Game, Scrap


class SendUrlForm(forms.Form):
    url = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Url',
                                                                                  }))


class UrlForm(ModelForm):
    link = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Url',
                                                                                   'type': 'text',
                                                                                   'name': 'displayValue',
                                                                                   'id': 'displayValue',
                                                                                   'onfocus': 'this.select()',
                                                                                   'style': 'position:absolute;top:0px;left:0px;width:90%;height:23px; height:21px\9;#height:18px;border:1px solid #556;'

                                                                                   }))

    class Meta:
        model = Game
        fields = ['link']
