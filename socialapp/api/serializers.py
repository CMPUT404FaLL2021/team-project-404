from rest_framework import serializers
from socialapp.models import Post

class PostSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Post
        fields = ['title', 'description', 'contentType', 'content', 'author', 'published', 'visibility', 'unlisted', 'id']