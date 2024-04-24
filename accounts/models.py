from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=245)
    thumbnail = models.ImageField(upload_to="sportImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_games = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_accounts = models.BooleanField(default=False)


class Championship(models.Model):
    name = models.CharField(max_length=245)
    thumbnail = models.ImageField(upload_to="champImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
