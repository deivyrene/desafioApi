from django.db import models
from django.utils import timezone


class Uf(models.Model):
    uf = models.CharField(max_length=255)
    date = models.DateField(null=True)

class Dolar(models.Model):
    dolar = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True)

class Tmc(models.Model):
    tmc = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True)