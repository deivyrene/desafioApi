from django.db import models
from django.utils import timezone


class Uf(models.Model):
    uf = models.CharField(max_length=25)
    date = models.DateField(null=True)

class Dolar(models.Model):
    dolar = models.CharField(max_length=25)
    date = models.DateField(null=True)

class Tmc(models.Model):
    tmc =  models.CharField(max_length=25)
    tipo_tmc = models.CharField(max_length=25, null=True)
    date = models.DateField(null=True)