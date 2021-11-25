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
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from socialapp.api import serializers

from socialapp.models import Author, Post, Comment, Like, Inbox, FriendRequest
from socialapp.api.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer

# reference: https://www.youtube.com/watch?v=wmYSKVWOOTM
# pagination, default page = 1, size = 5
def pagination(objects, request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', objects.count())
    objects_page = Paginator(objects, size)
    return objects_page.get_page(page)


@api_view(['GET'])
def api_authors_profile(request):
    if request.method == 'GET':
        data = {}
        data['type'] = 'authors'

        try:
            authors = Author.objects.all()
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # GET ://service/authors/
        if not request.query_params:
            serializer = AuthorSerializer(authors, many=True)
            data['items'] = serializer.data
            return Response(data=data)
            
        # GET ://service/authors?page=10&size=5
        if request.query_params:
            authors_page = pagination(authors, request)
            serializer = AuthorSerializer(authors_page, many=True)
            data['items'] = serializer.data
            return Response(data=data)


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_author_detail(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET //service/author/{AUTHOR_ID}/ 
    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    
    # POST //service/author/{AUTHOR_ID}/
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(author,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_author_followers(request, author_id):
    if request.method == 'GET':
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # GET //service/author/{AUTHOR_ID}/followers
        data = {}
        data['type'] = 'followers'
        followers = author.followers.all()
        serializer = AuthorSerializer(followers, many=True)
        data['items'] = serializer.data

        return Response(data=data)


@api_view(['DELETE', 'PUT', 'GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_author_follower(request, author_id, follower_id):
    try:
        follower = Author.objects.get(id=follower_id)
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if follower not in author.followers.all():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET //service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    if request.method == 'GET':
        serializer = AuthorSerializer(follower)
        return Response(serializer.data)
    
    # PUT //service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    if request.method == 'PUT':
        author.followers.add(follower)
        data = {}
        data['success'] = "Put successfully"
        return Response(data=data)

    # DELETE //service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    if request.method == 'DELETE':
        author.followers.remove(follower)
        data = {}
        data['success'] = "Delete successfully"
        return Response(data=data)


@api_view(['POST'])
def api_author_follows(request, author_id, follows_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        try:
            author_to_follow = Author.objects.get(id=follows_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        author_to_follow.followers.add(author)

        data = {}
        data['type'] = "Follow"
        data['summary'] = author.displayName + " wants to follow " + author_to_follow.displayName
        serializer1 = AuthorSerializer(author)
        serializer2 = AuthorSerializer(author_to_follow)
        data['actor'] = serializer1.data
        data['object'] = serializer2.data

        return Response(data=data)


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


@api_view(['GET', 'POST'])
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
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            new_post = serializer.save()
            new_post.author = Author.objects.get(id=author_id)
            new_post.save()
            data['success'] = 'Updated Successfully'
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_post_detail(request, author_id, post_id):
    # GET get the public post
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # POST update the post (must be authenticated)
    # missing authenticating step
    elif request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        operation = post.delete()
        data = {}
        if operation:
            data['success'] = "Delete successfully"
        else:
            data['failure'] = "Delete failed"
        return Response(data=data)

    # PUT create a post with that post_id
        # PUT create a post with that post_id
    elif request.method == 'PUT':
        try:
            post = Post.objects.get(id=post_id)
            return Response("Post already exists.", status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            pass
            
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            new_post = serializer.save()
            new_post.id = post_id
            new_post.author = Author.objects.get(id=author_id)
            new_post.save()
            data['success'] = 'Updated Successfully'
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_post_like(request, author_id, post_id):
    try:
        post = Post.objects.get(id=post_id)
        # author = Author.objects.get(id=author_id)
    except Post.DoesNotExist or Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        likes = Like.objects.filter(object=post)
        if likes.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes_page = pagination(likes, request)
        serializer = LikeSerializer(likes_page, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_likes(request, author_id):
    liked = Post.objects.filter(likes=author_id)
    if liked.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        liked_page = pagination(liked, request)
        serializer = PostSerializer(liked_page, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def api_author_inbox(request, author_id):
    try:
        inbox = Inbox.objects.get(author=Author.objects.get(id=author_id))
    except Inbox.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET //service/author/{AUTHOR_ID}/inbox 
    if request.method == 'GET':
        posts = Post.objects.filter(inbox=inbox)
        if posts.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        posts_page = pagination(posts, request)
        serializer = PostSerializer(posts_page, many=True)
        data = {}
        data['type'] = 'inbox'
        data['author'] = author_id
        data['items'] = serializer.data
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        if data['type'] == 'post':
            try:
                post = Post.objects.get(id=data['id'])
            except Post.DoesNotExist:
                id = data['id']
                title = data['title']
                content = data['content']
                description = data['description']
                visibility = data['visibility']
                contentType = data['contentType']
                unlisted = data['unlisted']
                post = Post(id=id, title=title, content=content, description=description, author=Author.objects.get(id=data['author']['id']), visibility=visibility, unlisted=unlisted, contentType=contentType)

            post.save()
            post.inbox.add(inbox)
            return HttpResponse('Success')
        
        elif data['type'] == 'like':
            try:
                post = Post.objects.get(id=data['object'])
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            l = Like(author=Author.objects.get(id=data['author']['id']), object=post)
            l.save()
            post.likes.add(Author.objects.get(id=data['author']['id']))
            return HttpResponse('Success')

        elif data['type'] == 'follow':
            try:
                actor = Author.objects.get(id=data['actor']['id'])
                object = Author.objects.get(id=data['object']['id'])
            except Author.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            try:
                FriendRequest.objects.get(actor=actor,object=object)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(actor=actor, object=object, inbox=Inbox.objects.get(author=object))
                friend_request.save()
                return Response(data=data)

            data = {}
            data['Failed':'Friend Request already existed.']
            return Response(data=data)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        for p in Post.objects.filter(inbox=inbox):
            p.inbox.clear()
            return Response(data=data)
        FriendRequest.objects.filter(inbox=inbox).update(inbox=None)
        Comment.objects.filter(inbox=inbox).update(inbox=None)
        Like.objects.filter(inbox=inbox).update(inbox=None)
        data = {}
        data['message'] = 'Deleted'
        return Response(data=data)

    