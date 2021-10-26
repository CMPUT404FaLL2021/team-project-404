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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # source
    # origin
    description = models.CharField(max_length=140, default='')
    contentType = models.CharField(max_length=30, default='PLAIN')
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # categories
    published = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=30, default='PUBLIC')
    unlisted = models.BooleanField(default=False)
    #edit = models.CharField(max_length=140)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    
    def like_count(self):
        return self.likes.count()
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contentType = models.CharField(max_length=30, default='PLAIN')
    published = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)