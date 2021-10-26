# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import AuthorForm, PostForm, CommentForm
from socialapp.models import *
from django.urls import reverse
import datetime


# view of index.html
def index(request):
    authors = Author.objects.all()
    content = {'authors': authors}
    return render(request, "socialapp/index.html", content)

# view of main_page
def main_page(request, author_id):
    p_list = Post.objects.filter(visibility='PUBLIC').order_by('-published')

    return render(request, "socialapp/main_page.html", {'author_id':author_id, 'p_list':p_list})


# view of register.html
def register(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
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
        form = AuthorForm()
    return render(request, 'socialapp/register.html', {'form':form})


# view of login.html
def login(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        displayName = form.data['displayName']
        password = form.data['password']
        author = Author.objects.filter(displayName=displayName, password=password)
        if author:
            info = 'Login Successfully!'
            content = {'info':info}

            # set cookies
            response = redirect(main_page, author[0].id)
            response.set_cookie('displayName', displayName)
            return response 

        else:
            info = 'Login Failed!'
            content = {'info':info}
            return render(request, 'socialapp/index.html', content)
    else:
        form = AuthorForm()
    
    return render(request, 'socialapp/login.html', {'form':form})


# view of author_profile.html
def author_profile(request, author_id):
    if request.method == 'GET':
        me = Author.objects.get(pk=author_id)
        p_list = Post.objects.filter(author=me, unlisted=False, visibility='PUBLIC').order_by('-published')

    return render(request, "socialapp/author_profile.html", {'author': me, 'p_list': p_list})


# view of author_follows_me.html
def my_followers(request, author_id):
    if request.method == 'GET':
        me = Author.objects.get(pk=author_id)
        author_list = me.followers.all()

    return render(request, "socialapp/my_followers.html", {'author_id':author_id, 'author_list': author_list})


# view of author_I_follow.html
def my_follows(request, author_id):
    if request.method == 'GET':
        me = Author.objects.get(pk=author_id)
        author_list = []
        for author in Author.objects.all():
            if me in author.followers.all():
                author_list.append(author)
    return render(request, "socialapp/my_follows.html", {'author_id':author_id, 'author_list': author_list})


# view of my_friends.html
def my_friends(request, author_id):
    if request.method == 'GET':
        me = Author.objects.get(pk=author_id)
        author_list = []
        for author in me.followers.all():
            if me in author.followers.all():
                author_list.append(author)
    return render(request, "socialapp/my_friends.html", {'author_id':author_id, 'author_list': author_list})


# view of add_post.html
def add_post(request, author_id):
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
            p = Post(title=title, content=content, description=description, author=Author.objects.get(id=author_id), visibility=visibility, unlisted=unlisted, contentType=contentType)
            p.save()
            response = redirect(main_page, author_id)
            return response

    else:
        form = PostForm()

    return render(request, 'socialapp/add_post.html', {'form':form, 'author_id':author_id})     

def if_like(post_to_show, author_id):
    if post_to_show.likes.filter(id=author_id).exists():
        return True
    return False

def if_follow(post_to_show, author_id):
    post_author = post_to_show.author
    me = Author.objects.get(pk=author_id)
    followers = post_author.followers.all()
    if me in followers:
        return True
    return False

# view of show_post.html
def show_post(request, author_id, show_post_id):
    post_to_show = Post.objects.get(pk=show_post_id)
    post_comments = Comment.objects.filter(post=post_to_show).order_by("-published")
    context = {'post_to_show': post_to_show, 'author_id': author_id, 'post_comments':None, 'comment_count':0}
    if post_comments:
        context['post_comments'] = post_comments
        context['comment_count'] = post_comments.count()

    like_status = if_like(post_to_show, author_id)
    context['like_status'] = like_status
    follow_status = if_follow(post_to_show, author_id)
    context['follow_status'] = follow_status

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        context['form'] = form
        if 'like_button' in request.POST:
            if like_status:
                post_to_show.likes.remove(Author.objects.get(id=author_id))
            else:
                post_to_show.likes.add(Author.objects.get(id=author_id))

        elif 'post_button' in request.POST:
            comment = form.data['comment']
            if form.is_valid():
                comment = form.cleaned_data['comment']
                c = Comment(comment=comment, post=post_to_show, author=Author.objects.get(id=author_id))
                c.save()
        
        elif 'delete_comment' in request.POST:
            comment_id = request.POST['delete_comment']
            del_comment = Comment.objects.get(id=comment_id)
            del_comment.delete()

        elif 'share_post' in request.POST:
            author = Author.objects.get(id=author_id)
            content = ("%s forwarded %s's post:\n" % (author.displayName, post_to_show.author.displayName)) + post_to_show.content
            # visibility = 
            # unlisted = check_box.cleaned_data['check_box']
            p = Post(content=content, author=Author.objects.get(id=author_id))
            p.save()
            response = redirect(main_page, author_id)
            return response

        elif 'follow_button' in request.POST:
            me = Author.objects.get(pk=author_id)
            post_author = post_to_show.author
            if follow_status:
                post_author.followers.remove(me)
            else:
                post_author.followers.add(me)

        return HttpResponseRedirect(reverse('show_post', args=[author_id, show_post_id]))

    else:
        form = CommentForm()

    context['form'] = form
    return render(request, 'socialapp/show_post.html', context)


# view of edit_post.html
def edit_post(request, author_id, edit_post_id):
    post_to_show = Post.objects.get(pk=edit_post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            changed_post = form.cleaned_data['post']
            post_to_show.content = changed_post
            post_to_show.published = datetime.date.today()
            post_to_show.save()
            response = redirect(show_post, author_id, edit_post_id)
            return response
    else:
        form = PostForm(initial={"post":post_to_show.published})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_post.html', {'form':form, 'modified_post':post_to_show, 'author_id':author_id})


# view of logout.html
def logout(request):
    
    return redirect('/index/')