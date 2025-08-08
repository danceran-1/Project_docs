from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    username = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only letters, numbers and _ are allowed!')]
    )
    password = models.CharField(max_length=128) 

class UserAvatar(models.Model):
    user_id = models.IntegerField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PersonalDataAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agreed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Agreement from {self.user.username} at {self.agreed_at}"


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