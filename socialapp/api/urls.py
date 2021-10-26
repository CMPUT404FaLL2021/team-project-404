from django.urls import path
from socialapp.api import views

urlpatterns = [
    path('author/<uuid:author_id>/posts/<uuid:post_id>/', views.api_post_detail, name='post_detail')
]