# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import UserForm, PostForm, VisiChoices, CheckBox, CommentForm
from socialapp.models import *
from django.urls import reverse
import datetime


# view of index.html
def index(request):
    users = User.objects.all()
    content = {'users': users}
    return render(request, "socialapp/index.html", content)

# view of mainPage
def mainPage(request, username):
    # check if user_in in cookies
    p_list = Post.objects.filter(visibility='PUBLIC').order_by('-pk').values_list('post', 'user', 'date', 'pk')

    if 'username' not in request.COOKIES:
        return render(request, 'socialapp/login.html', {'form':UserForm()})
    username = request.COOKIES['username']
    return render(request, "socialapp/mainPage.html", {'username':username, 'p_list':p_list})


# view of register.html
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # check if the sign up process succeds
        if form.is_valid():
            form.save()
            #info = 'Sign Up Successfully!'
            #content = {'info':info}
            #return render(request, 'socialapp/login.html', content)
            #如果注册成功，重定向到login页面，展示“注册成功”信息 (详细在loing.html)
            messages.success(request, 'Sign up successfully!')
            return redirect(login)
        else:
            info = 'Sign Up Failed! Ivalid Username or Password'
            content = {'info':info}
            return render(request, 'socialapp/index.html', content)
    else:
        form = UserForm()
    return render(request, 'socialapp/register.html', {'form':form})


# view of login.html
def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        user = User.objects.filter(username=username, password=password)
        if user:
            info = 'Login Successfully!'
            content = {'info':info}

            # set cookies
            response = redirect(mainPage, username)
            response.set_cookie('username', username)
            return response 

        else:
            info = 'Login Failed!'
            content = {'info':info}
            return render(request, 'socialapp/index.html', content)
    else:
        form = UserForm()
    
    return render(request, 'socialapp/login.html', {'form':form})


# view of user_profile.html
def user_profile(request, username):
    if request.method == 'GET':
        # check if user_id recored in cookies
        if 'username' not in request.COOKIES:
            return render(request, 'socialapp/login.html', {'form':UserForm()})
        username = request.COOKIES['username']
    # other methods might need to be handled at here
    else:
        pass

    return render(request, "socialapp/user_profile.html", {'username':username})


# view of add_post.html
def add_post(request):
    # check if user_in in cookies
    if 'username' not in request.COOKIES:
        return render(request, 'socialapp/login.html', {'form':UserForm()})
    username = request.COOKIES['username']

    if request.method == 'POST':
        form = PostForm(request.POST)
        visibility = VisiChoices(request.POST)
        check_box = CheckBox(request.POST)
        # read and save inputs
        if form.is_valid() and visibility.is_valid() and check_box.is_valid():
            post = form.cleaned_data['post']
            visibility = visibility.cleaned_data['visibility']
            unlisted = check_box.cleaned_data['check_box']
            p = Post(post=post, user=User.objects.get(username=username), visibility=visibility, unlisted=unlisted)
            p.save()
            response = redirect(mainPage)
            return response

    else:
        form = PostForm()
        visibility = VisiChoices()
        check_box = CheckBox()

    return render(request, 'socialapp/add_post.html', {'form':form, 'visibility':visibility, 'check_box':check_box, 'username':username})     

def if_like(post_to_show, username):
    if post_to_show.likes.filter(username=username).exists():
        return True
    return False

# view of show_post.html
def show_post(request, show_post_id):
    # check authorization
    if 'username' not in request.COOKIES:
        return render(request, 'socialapp/login.html', {'form':UserForm()})
    username = request.COOKIES['username']

    post_to_show = Post.objects.get(pk=show_post_id)
    post_comments = Comment.objects.filter(post=post_to_show).order_by("-date").values_list('comment', 'user', 'date', 'id')
    context = {'post_to_show': post_to_show, 'username': username, 'post_comments':post_comments}

    like_status = if_like(post_to_show, username)
    context['like_status'] = like_status

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        context['form'] = form
        if 'like_button' in request.POST:
            if like_status:
                post_to_show.likes.remove(User.objects.get(username=username))
            else:
                post_to_show.likes.add(User.objects.get(username=username))

        elif 'post_button' in request.POST:
            comment = form.data['comment']
            if form.is_valid():
                comment = form.cleaned_data['comment']
                c = Comment(comment=comment, post=post_to_show, user=User.objects.get(username=username))
                c.save()
        
        elif 'delete_comment' in request.POST:
            id = request.POST['delete_comment']
            del_comment = Comment.objects.get(id=id)
            del_comment.delete()

        elif 'share_post' in request.POST:
            post = ("%s forwarded %s's post:\n" % (username, post_to_show.user.username)) + post_to_show.post
            # visibility = 
            # unlisted = check_box.cleaned_data['check_box']
            p = Post(post=post, user=User.objects.get(username=username))
            p.save()
            response = redirect(mainPage)
            return response

        return HttpResponseRedirect(reverse('show_post', args=[show_post_id]))

    else:
        form = CommentForm()

    context['form'] = form
    return render(request, 'socialapp/show_post.html', context)


# view of edit_post.html
def edit_post(request, edit_post_id):
    post_to_show = Post.objects.get(pk=edit_post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            changed_post = form.cleaned_data['post']
            post_to_show.post = changed_post
            post_to_show.date = datetime.date.today()
            post_to_show.save()
            response = redirect(show_post, edit_post_id)
            return response
    else:
        form = PostForm(initial={"post":post_to_show.post})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_post.html', {'form':form, 'modified_post':post_to_show})


# view of logout.html
def logout(request):
    
    return redirect('/index/')