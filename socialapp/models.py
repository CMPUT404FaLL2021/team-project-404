from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    friends = models.ManyToManyField("self", symmetrical=False)

class Post(models.Model):
    post = models.CharField(max_length=140)
    # username = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=timezone.now)
    visibility = models.CharField(max_length=30, default='PUBLIC')
    unlisted = models.BooleanField(default=False)
    #edit = models.CharField(max_length=140)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    comment = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)