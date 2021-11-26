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
    path('author_inbox/<uuid:author_id>/', views.author_inbox, name = 'author_inbox'),
    path('add_post/<uuid:author_id>/', views.add_post, name = 'add_post'),
    path('select_views/<uuid:author_id>/<uuid:post_id>/', views.select_viewers, name = 'select_viewers'),
    path('edit_post/<uuid:author_id>/<uuid:edit_post_id>/', views.edit_post, name = 'edit_post'),
    path('show_post/<uuid:author_id>/<uuid:show_post_id>/', views.show_post, name = 'show_post'),
    path('author_profile/<uuid:author_id>/', views.author_profile, name = 'author_profile'),
    path('edit_profile/<uuid:author_id>/', views.edit_profile, name = 'edit_profile'),
    path('main_page/<uuid:author_id>/', views.main_page, name = 'main_page'),
    path('my_followers/<uuid:author_id>/', views.my_followers, name  = 'my_followers'),
    path('my_follows/<uuid:author_id>/', views.my_follows, name  = 'my_follows'),
    path('my_friends/<uuid:author_id>/', views.my_friends, name  = 'my_friends'),
]
