# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import UserForm, PostForm
from socialapp.models import *
import datetime

chosen_post = 5

# view of index.html
def index(request):
    users = User.objects.all()
    content = {'users': users}
    return render(request, "socialapp/index.html", content)


# view of register.html
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            info = 'Sign Up Successfully!'
            content = {'info':info}
            return render(request, 'socialapp/index.html', content)
            #return HttpResponse('Sign Up Successfully!')
        else:
            info = 'Sign Up Failed!'
            content = {'info':info}
            return render(request, 'socialapp/index.html', content)
            #return HttpResponse(form.errors)
    else:
        form = UserForm()
    return render(request, 'socialapp/register.html', {'form':form})


# view of login.html
def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username, password=password)
            if user:
                info = 'Login Successfully!'
                content = {'info':info}

                # set cookies
                response = redirect(show_post) # testing only, should set cookies go to main page
                response.set_cookie('username', username, max_age=60)
                return response 

            else:
                info = 'Login Failed!'
                content = {'info':info}
                return render(request, 'socialapp/index.html', content)
    else:
        form = UserForm()
    
    return render(request, 'socialapp/login.html', {'form':form})


# view of user_profile.html
def user_profile(request):
    username = 'unknown'
    if request.method == 'GET':
        # check if user_id recored in cookies
        if 'username' not in request.COOKIES:
            return render(request, 'socialapp/login.html', {'form':UserForm()})
        username = request.COOKIES['username']
    # other methods might need to be handled at here
    else:
        # might subject to change
        # return redirect(login)
        pass

    return render(request, "socialapp/user_profile.html", {'username':username})


# view of add_post.html
def add_post(request):
    # check if cookie valid
    if 'username' not in request.COOKIES:
        return render(request, 'socialapp/login.html', {'form':UserForm()})
    username = request.COOKIES['username']
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data['post']
            p = Post(post=post, username=username)
            p.save()
        return HttpResponse(p.post)
    else:
        form = PostForm()

    return render(request, 'socialapp/add_post.html', {'form':form})     


# view of show_post.html
def show_post(request):
    post_to_show = Post.objects.get(pk=chosen_post)
    post_info = "Content: %s\n\nAuthor: %s\n\nDate: %s" % (post_to_show.post, post_to_show.username, post_to_show.date)
    #id_content = {'num':chosen_post}
    content = {'info':post_info}
    return render(request, 'socialapp/show_post.html', content)


# view of edit_post.html
def edit_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            changed_post = form.cleaned_data['post']
            p = Post.objects.get(pk=chosen_post)
            p.post = changed_post
            p.date = datetime.date.today()
            p.save()
            response = redirect(show_post)
            return response
    else:
        form = PostForm()

    return render(request, 'socialapp/edit_post.html', {'form':form})


# view of logout.html
def logout(request):
    
    return redirect('/index/')