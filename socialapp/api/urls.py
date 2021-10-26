from django.urls import path
from socialapp.api import views

urlpatterns = [
    path('author/<uuid:author_id>/', views.api_author_detail, name='author_detail'),
    path('author/<uuid:author_id>/posts/<uuid:post_id>/comments/', views.api_post_comments, name='comments_detail'),
    path('author/<uuid:author_id>/posts/<uuid:post_id>/likes/', views.api_post_like, name='post_like'),
    path('author/<uuid:author_id>/posts/<uuid:post_id>/', views.api_post_detail, name='post_detail'),
]