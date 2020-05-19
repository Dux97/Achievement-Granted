from django.db import models

# Create your models here.
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=200)


class Scrap(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    fandom_url = models.CharField(max_length=200)
    gamepedia_url = models.CharField(max_length=200)
    xboxachiev_url = models.CharField(max_length=200)
    trueachiev_url = models.CharField(max_length=200)
