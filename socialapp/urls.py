from django.contrib import admin
from django.urls import path
from socialapp.views import index
from . import views

urlpatterns = [
    #path('admin/', admin.side.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('add_post/<uuid:author_id>/', views.add_post, name = 'add_post'),
    path('edit_post/<uuid:author_id>/<uuid:edit_post_id>/', views.edit_post, name = 'edit_post'),
    path('show_post/<uuid:author_id>/<uuid:show_post_id>/', views.show_post, name = 'show_post'),
    path('author_profile/<uuid:author_id>/', views.author_profile, name = 'author_profile'),
    path('main_page/<uuid:author_id>/', views.main_page, name = 'main_page'),
    path('author_follows_me/<uuid:author_id>/', views.author_follows_me, name  = 'author_follows_me'),
    path('author_I_follow/<uuid:author_id>/', views.author_I_follow, name  = 'author_I_follow'),
    path('my_friends/<uuid:author_id>/', views.my_friends, name  = 'my_friends')
]
