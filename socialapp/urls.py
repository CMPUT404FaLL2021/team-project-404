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
    path('add_post/', views.add_post, name = 'add_post'),
    path('edit_post/', views.edit_post, name = 'edit_post'),
    path('show_post/', views.show_post, name = 'show_post')
]
