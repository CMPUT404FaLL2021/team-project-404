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
    path('add_post/<uuid:user_id>/', views.add_post, name = 'add_post'),
    path('edit_post/<uuid:user_id>/<uuid:edit_post_id>/', views.edit_post, name = 'edit_post'),
    path('show_post/<uuid:user_id>/<uuid:show_post_id>/', views.show_post, name = 'show_post'),
    path('user_profile/<uuid:user_id>/', views.user_profile, name = 'user_profile'),
    path('main_page/<uuid:user_id>/', views.main_page, name = 'main_page'),
    path('user_follows_me/<uuid:user_id>/', views.user_follows_me, name  = 'user_follows_me'),
    path('user_I_follow/<uuid:user_id>/', views.user_I_follow, name  = 'user_I_follow'),
    path('my_friends/<uuid:user_id>/', views.my_friends, name  = 'my_friends')
]
