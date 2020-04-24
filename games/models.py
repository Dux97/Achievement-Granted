from django.db import models

# Create your models here.
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=200)
    wiki_url = models.CharField(max_length=200)


class Scrap(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    table_html = models.CharField(max_length=200)
    achievement_html = models.CharField(max_length=200)
