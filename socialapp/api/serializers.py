from rest_framework import serializers
from socialapp.models import Author, Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    @classmethod
    def get_type(self, object):
        return 'author'
    class Meta:
        model = Author
        fields = ['type', 'id', 'displayName']

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    @classmethod
    def get_type(self, object):
        return 'comment'
    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id']

class PostSerializer(serializers.ModelSerializer): 
    type = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    count = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    @classmethod
    def get_type(self, object):
        return 'post'
    
    def get_count(self, object):
        return Comment.objects.filter(post=object).count()

    def get_comment(self, object):
        return CommentSerializer(Comment.objects.filter(post=object), many=True).data

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'description', 'contentType', 'content', 'author', 'count', 'comment', 'published', 'visibility', 'unlisted']

