from django.db import models

from django.conf import settings


class Dialogue(models.Model):
    user = models.CharField(max_length=256)
    bot = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)