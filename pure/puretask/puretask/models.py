from django.contrib.postgres.fields import JSONField
from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=20)

class Car(models.Model):
    parameters = JSONField()

