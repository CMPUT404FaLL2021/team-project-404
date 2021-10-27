import uuid
from django.db import models
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    displayName = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    # profileImage =
    # host =
    # url =
    # github =
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)


class Inbox(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=140, default='')
    # source
    # origin
    description = models.CharField(max_length=140, default='')
    contentType = models.CharField(max_length=30, default='PLAIN')
    content = models.CharField(max_length=140)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    # categories
    published = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=30, default='PUBLIC')
    unlisted = models.BooleanField(default=False)
    #edit = models.CharField(max_length=140)
    likes = models.ManyToManyField(Author, related_name='post_likes', blank=True)
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, null=True)
    
    def like_count(self):
        return self.likes.count()
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contentType = models.CharField(max_length=30, default='PLAIN')
    published = models.DateTimeField(default=timezone.now)