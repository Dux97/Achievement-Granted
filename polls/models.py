from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)


class ScrapPattern(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    table = models.CharField(max_length=200)
    archvement = models.CharField(max_length=200)
