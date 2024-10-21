# cats/models.py
from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    gender = models.CharField(max_length=32)
