from django.contrib import admin
from socialapp import models
# Register your models here.

admin.site.register(models.Author)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Inbox)
admin.site.register(models.FriendRequest)
