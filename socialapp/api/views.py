from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from socialapp.models import Post, User
from socialapp.api.serializers import PostSerializer

@api_view(['GET', 'POST'])
def api_post_detail(request, author_id, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['id'] = post_id
        serializer = PostSerializer(post,data=data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'Updated Successfully'
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
