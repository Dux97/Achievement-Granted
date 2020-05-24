from django.db import models

# Create your models here.
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200, null=True, unique=True)


class Scrap(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    otherlink = models.CharField(max_length=200)
