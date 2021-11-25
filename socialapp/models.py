'''
in thjis file we create the models used to collcet the data easier 
and use the models in views.py
'''

import uuid
from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
import markdown

# Author model
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    displayName = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to = 'avatar', blank=True)
    host = models.URLField(max_length=64, default="http://cmput404-team13-socialapp.herokuapp.com")
    url = models.URLField(max_length=100, default='http://cmput404-team13-socialapp.herokuapp.com/author/')
    github = models.CharField(max_length=100, blank = True)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)

#Inbox model
class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

#froends model
class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='frieqnd_request_object', null=True)
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, null=True, blank=True)

#post model
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=140, default='')
    source = models.URLField(default='https://cmput404-team13-socialapp.herokuapp.com/')
    origin = models.URLField(default='https://cmput404-team13-socialapp.herokuapp.com/')
    description = models.CharField(max_length=140, default='')
    contentType = models.CharField(max_length=30, default='PLAIN')
    content = MDTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    categories = models.CharField(max_length=100, blank=True)
    published = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=30, default='PUBLIC')
    unlisted = models.BooleanField(default=False)
    #edit = models.CharField(max_length=140)
    likes = models.ManyToManyField(Author, related_name='post_likes', blank=True)
    inbox = models.ManyToManyField(Inbox, blank=True)
    
    def like_count(self):
        return self.likes.count()

    def get_markdown_content(self):
        return markdown.markdown(self.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    
#comment model
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contentType = models.CharField(max_length=30, default='PLAIN')
    published = models.DateTimeField(default=timezone.now)
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, null=True, blank=True)

class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, default='Like')
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, null=True, blank=True)