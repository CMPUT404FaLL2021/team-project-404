'''
this file set the api serializer
function includes:

AuthorSerializer
CommentSerializer
PostSerializer
LikeSerializer
'''

from rest_framework import serializers
from socialapp.models import Author, FriendRequest, Post, Comment, Like


#set the serializer of Author
class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    @classmethod
    def get_type(self, object):
        return 'author'
    class Meta:
        model = Author
        fields = ['type', 'id', 'displayName', 'url', 'host', 'github', 'avatar']


#set the serializer of Comments
class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    @classmethod
    def get_type(self, object):
        return 'comment'
    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id']


#set the serializer of Post
class PostSerializer(serializers.ModelSerializer): 
    type = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    count = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    @classmethod
    def get_type(self, object):
        return 'post'
    
    def get_count(self, object):
        return Comment.objects.filter(post=object).count()

    def get_comment(self, object):
        return CommentSerializer(Comment.objects.filter(post=object), many=True).data

    def get_url(self, object):
        return object.origin + 'api/author/' + str(object.author.id) + '/posts/' + str(object.id) + '/'

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'url', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'count', 'comment', 'published', 'visibility', 'unlisted']


class LikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    summary = serializers.SerializerMethodField()
    @classmethod
    def get_summary(self, object):
        return object.author.displayName + ' likes your post.'

    class Meta:
        model = Like
        fields = ['summary', 'type', 'author', 'object']


class FriendRequestSerialier(serializers.ModelSerializer):
    actor = AuthorSerializer(read_only=True)
    object = AuthorSerializer(read_only=True)
    type = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    @classmethod
    def get_type(self, this_object):
        return 'follow'
    def get_summary(self, this_object):
        return this_object.actor.displayName + 'wants to follow' + this_object.object.displayName
    
    class Meta:
        model = FriendRequest
        fields = ['type', 'summary', 'actor', 'object']