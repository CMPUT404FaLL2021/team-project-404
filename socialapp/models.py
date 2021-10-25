import uuid
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    # user_image =
    # host =
    # url =
    # github =
    friends = models.ManyToManyField("self", symmetrical=False)

class Post(models.Model):
    title = models.CharField(max_length=140, default='')
    description = models.CharField(max_length=140, default='')
    post = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=30, default='PUBLIC')
    content_type = models.CharField(max_length=30, default='PLAIN')
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