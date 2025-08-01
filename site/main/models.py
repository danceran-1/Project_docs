from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    username = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only letters, numbers and _ are allowed!')]
    )
    password = models.CharField(max_length=128) 

class CalculationResult(models.Model):
    A = models.IntegerField()
    B = models.IntegerField()
    K1 = models.FloatField()
    mark = models.IntegerField()
    A1 = models.IntegerField()
    B1 = models.IntegerField()
    K2 = models.FloatField()
    mark1 = models.IntegerField()
class Criterion(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/')