'''
this file set the api of the function in views.py 
includes:
auther_details
post_comments
post_details
post_like
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from socialapp.models import Author, Post, Comment
from socialapp.api.serializers import AuthorSerializer, PostSerializer, CommentSerializer

@api_view(['GET', 'POST'])
def api_author_detail(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_post_comments(request, author_id, post_id):
    try:
        comments = Comment.objects.filter(post=post_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET get comments of the post
    if request.method == 'GET':
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'DELETE'])
def api_post_detail(request, author_id, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET get the public post
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # POST update the post (must be authenticated)
    # missing authenticating step
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['id'] = post_id
        serializer = PostSerializer(post,data=data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'Updated Successfully'
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE remove the post
    elif request.method == 'DELETE':
        operation = post.delete()
        data = {}
        if operation:
            data['success'] = "Delete successfully"
        else:
            data['failure'] = "Delete failed"
        return Response(data=data)

    # PUT create a post with that post_id

@api_view(['GET'])
def api_post_like(request, author_id, post_id):
    try:
        post = Post.objects.get(id=post_id)
        author = Author.objects.get(id=author_id)
    except Post.DoesNotExist or Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = {}
    if request.method == 'GET':
        data['summary'] = author.displayName + 'Likes your post'
        data['type'] = 'like'
        data['author'] = AuthorSerializer(author).data
        data['object'] = post_id
        return Response(data=data)