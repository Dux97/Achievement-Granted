import datetime

from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.game_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class ScrapPattern(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    table = models.CharField(max_length=200)
    archvement = models.CharField(max_length=200)

    def __str__(self):
        return self.ScrapPattern_text
