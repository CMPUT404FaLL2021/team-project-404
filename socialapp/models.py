from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Post(models.Model):
    post = models.CharField(max_length=140)
    username = models.CharField(max_length=32)
    date = models.DateField(default=timezone.now)
    friends_only = models.BooleanField(default=False)