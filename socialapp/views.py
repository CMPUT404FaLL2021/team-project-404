# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import UserForm, PostForm, CommentForm
from socialapp.models import *
from django.urls import reverse
import datetime


# view of index.html
def index(request):
    users = User.objects.all()
    content = {'users': users}
    return render(request, "socialapp/index.html", content)

# view of main_page
def main_page(request, user_id):
    # check if user_in in cookies
    p_list = Post.objects.filter(visibility='PUBLIC').order_by('-pk').values_list('content', 'author', 'published', 'pk')

    return render(request, "socialapp/main_page.html", {'user_id':user_id, 'p_list':p_list})


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
            response = redirect(main_page, user[0].user_id)
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
def user_profile(request, user_id):
    if request.method == 'GET':
        me = User.objects.get(pk=user_id)
        p_list = Post.objects.filter(user=me, unlisted=False).order_by('-pk').values_list('post', 'user', 'date', 'pk')

    return render(request, "socialapp/user_profile.html", {'user': me, 'p_list': p_list})


# view of user_follows_me.html
def user_follows_me(request, user_id):
    if request.method == 'GET':
        me = User.objects.get(pk=user_id)
        user_list = []
        for user in User.objects.all():
            if me in user.friends.all():
                user_list.append(user)

    return render(request, "socialapp/user_follows_me.html", {'user_id':user_id, 'user_list': user_list})


# view of user_I_follow.html
def user_I_follow(request, user_id):
    if request.method == 'GET':
        me = User.objects.get(pk=user_id)
        user_list = me.friends.all()
    return render(request, "socialapp/user_I_follow.html", {'user_id':user_id, 'user_list': user_list})


# view of my_friends.html
def my_friends(request, user_id):
    if request.method == 'GET':
        me = User.objects.get(pk=user_id)
        user_list = []
        for user in me.friends.all():
            if me in user.friends.all():
                user_list.append(user)
    return render(request, "socialapp/my_friends.html", {'user_id':user_id, 'user_list': user_list})


# view of add_post.html
def add_post(request, user_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        # read and save inputs
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            description = form.cleaned_data['description']
            visibility = form.cleaned_data['visibility']
            contentType = form.cleaned_data['contentType']
            unlisted = form.cleaned_data['unlisted']
            p = Post(title=title, content=content, description=description, author=User.objects.get(user_id=user_id), visibility=visibility, unlisted=unlisted, contentType=contentType)
            p.save()
            response = redirect(main_page, user_id)
            return response

    else:
        form = PostForm()

    return render(request, 'socialapp/add_post.html', {'form':form, 'user_id':user_id})     

def if_like(post_to_show, user_id):
    if post_to_show.likes.filter(user_id=user_id).exists():
        return True
    return False

# view of show_post.html
def show_post(request, user_id, show_post_id):
    post_to_show = Post.objects.get(pk=show_post_id)
    post_comments = Comment.objects.filter(post=post_to_show).order_by("-published").values_list('comment', 'author', 'published', 'id')
    comment_author = User.objects.get(user_id=post_comments[0][1]).username
    context = {'post_to_show': post_to_show, 'user_id': user_id, 'post_comments':post_comments, 'comment_count':post_comments.count(), 'comment_author':comment_author}

    like_status = if_like(post_to_show, user_id)
    context['like_status'] = like_status

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        context['form'] = form
        if 'like_button' in request.POST:
            if like_status:
                post_to_show.likes.remove(User.objects.get(user_id=user_id))
            else:
                post_to_show.likes.add(User.objects.get(user_id=user_id))

        elif 'post_button' in request.POST:
            comment = form.data['comment']
            if form.is_valid():
                comment = form.cleaned_data['comment']
                c = Comment(comment=comment, post=post_to_show, author=User.objects.get(user_id=user_id))
                c.save()
        
        elif 'delete_comment' in request.POST:
            id = request.POST['delete_comment']
            del_comment = Comment.objects.get(id=id)
            del_comment.delete()

        elif 'share_post' in request.POST:
            user = User.objects.get(user_id=user_id)
            content = ("%s forwarded %s's post:\n" % (user.username, post_to_show.author.username)) + post_to_show.content
            # visibility = 
            # unlisted = check_box.cleaned_data['check_box']
            p = Post(content=content, author=User.objects.get(user_id=user_id))
            p.save()
            response = redirect(main_page, user_id)
            return response

        elif 'follow_button' in request.POST:
            me = User.objects.get(pk=user_id)
            me.friends.add(post_to_show.author)

        return HttpResponseRedirect(reverse('show_post', args=[user_id, show_post_id]))

    else:
        form = CommentForm()

    context['form'] = form
    return render(request, 'socialapp/show_post.html', context)


# view of edit_post.html
def edit_post(request, user_id, edit_post_id):
    post_to_show = Post.objects.get(pk=edit_post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            changed_post = form.cleaned_data['post']
            post_to_show.content = changed_post
            post_to_show.published = datetime.date.today()
            post_to_show.save()
            response = redirect(show_post, user_id, edit_post_id)
            return response
    else:
        form = PostForm(initial={"post":post_to_show.published})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_post.html', {'form':form, 'modified_post':post_to_show, 'user_id':user_id})


# view of logout.html
def logout(request):
    
    return redirect('/index/')