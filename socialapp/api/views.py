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
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from socialapp.models import Author, Post, Comment
from socialapp.api.serializers import AuthorSerializer, PostSerializer, CommentSerializer

# reference: https://www.youtube.com/watch?v=wmYSKVWOOTM
# pagination, default page = 1, size = 5
def pagination(objects, request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 5)
    objects_page = Paginator(objects, size)
    return objects_page.get_page(page)

@api_view(['GET'])
def api_authors_profile(request):
    data = {}
    data['type'] = 'authors'
    data['items'] = []

    # GET ://service/authors/
    if not request.query_params:
        try:
            authors = Author.objects.all()
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for author in authors:
            serializer = AuthorSerializer(author)
            data['items'].append(serializer.data)
        
    # GET ://service/authors?page=10&size=5
    print(request.query_params)
    
    return Response(data=data)

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
        comments_page = pagination(comments, request)
        serializer = CommentSerializer(comments_page, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_posts(request, author_id):
    try:
        posts = Post.objects.filter(author=author_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        posts_page = pagination(posts, request)
        serializer = PostSerializer(posts_page, many=True)
        print(posts)
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
            return Response(data=data)
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