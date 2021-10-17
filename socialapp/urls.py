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
    path('add_post/<str:username>/', views.add_post, name = 'add_post'),
    path('edit_post/<str:username>/<int:edit_post_id>/', views.edit_post, name = 'edit_post'),
    path('show_post/<str:username>/<int:show_post_id>/', views.show_post, name = 'show_post'),
    path('user_profile/<str:username>/', views.user_profile, name = 'user_profile'),
    path('mainPage/<str:username>/', views.mainPage, name = 'mainPage'),
    path('user_follows_me/<str:username>/', views.user_follows_me, name  = 'user_follows_me'),
    path('user_I_follow/<str:username>/', views.user_I_follow, name  = 'user_I_follow'),
    path('my_friends/<str:username>/', views.my_friends, name  = 'my_friends')
]
