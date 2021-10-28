# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import AuthorForm, PostForm, CommentForm, ViewerForm
from socialapp.models import *
from django.urls import reverse
from django.utils import timezone


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
        name = form.data['displayName']
        # check if the sign up process succeds
        if form.is_valid():
            form.save()
            #info = 'Sign Up Successfully!'
            #content = {'info':info}
            #return render(request, 'socialapp/login.html', content)
            #如果注册成功，重定向到login页面，展示“注册成功”信息 (详细在loing.html)
            messages.success(request, 'Sign up successfully!')
            inbox = Inbox(author=Author.objects.get(displayName=name))
            inbox.save()
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


# view of inbox.html
def inbox(request, author_id):
    author = Author.objects.get(pk=author_id)
    inbox = Inbox.objects.get(author=author)
    friend_request_list = FriendRequest.objects.filter(inbox=inbox)
    posts = Post.objects.filter(inbox=inbox)

    if request.method == 'POST':
        for friend_request in friend_request_list:
            if 'follow_button_' + friend_request.actor.displayName in request.POST:
                friend_request.actor.followers.add(author)

    return render(request, 'socialapp/inbox.html', {'author_id': author_id, 'friend_request_list': friend_request_list, 'posts':posts})


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
            if visibility == "FRIENDS":
                friends = Author.objects.get(id=author_id).followers.all()
                for friend in friends:
                    inbox = Inbox.objects.get(author=Author.objects.get(id=friend.id))
                    p.inbox.add(inbox)
            elif visibility == "PRIVATE":
                return render(request, 'socialapp/select_viewers.html', {'form':ViewerForm, 'author_id':author_id, 'post_id':p.id})

            response = redirect(main_page, author_id)
            return response

    else:
        form = PostForm()

    return render(request, 'socialapp/add_post.html', {'form':form, 'author_id':author_id})  

def select_viewers(request, author_id, post_id):
    if request.method == 'POST':
        form = ViewerForm()
        post = Post.objects.get(id=post_id)
        """
        cannot not figure out why form.is_valid() always returns false
        """
        # if form.is_valid():
        #     return HttpResponse("test")
            # for viewer in viewers:
                # inbox = Inbox(author=Author.objects.get(id=viewer), post=post, type='post', message='Private Post')
                # inbox.save()
            # response = redirect(main_page, author_id)
            # return response
        viewer = request.POST.get('viewer', '')
        post = Post.objects.get(id=post_id)
        inbox = Inbox.objects.get(author=Author.objects.get(id=viewer))
        post.inbox.add(inbox)
        response = redirect(main_page, author_id)
        return response

    else:
        form = ViewerForm()

    return render(request, 'socialapp/select_viewers.html', {'form':form, 'author_id':author_id, 'post_id':post_id})
   

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
    if request.method == 'GET' and 'delete_button' in request.GET:
        post_to_show.delete()
        response = redirect(main_page, author_id)
        return response

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
            content = post_to_show.content + ("\n(%s forwarded %s's post)" % (author.displayName, post_to_show.author.displayName))
            # visibility = 
            # unlisted = check_box.cleaned_data['check_box']
            p = Post(title=post_to_show.title, description=post_to_show.description, content=content, author=Author.objects.get(id=author_id))
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
                friend_request = FriendRequest(actor=me, object=post_author, inbox=Inbox.objects.get(author=post_author))
                friend_request.save()

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
            changed_title = form.cleaned_data['title']
            changed_content = form.cleaned_data['content']
            changed_description = form.cleaned_data['description']
            changed_visibility = form.cleaned_data['visibility']
            changed_contentType = form.cleaned_data['contentType']
            changed_unlisted = form.cleaned_data['unlisted']
            post_to_show.title = changed_title
            post_to_show.description = changed_description
            post_to_show.content = changed_content
            post_to_show.visibility = changed_visibility
            post_to_show.contentType = changed_contentType
            post_to_show.unlisted = changed_unlisted
            post_to_show.published = timezone.now()
            post_to_show.save()
            response = redirect(show_post, author_id, edit_post_id)
            return response
    else:
        form = PostForm(initial={"title":post_to_show.title, "content":post_to_show.content, "description":post_to_show.description, "visibility":post_to_show.visibility, "contentType":post_to_show.contentType, "unlisted":post_to_show.unlisted})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_post.html', {'form':form, 'modified_post':post_to_show, 'author_id':author_id})


# view of logout.html
def logout(request):
    
    return redirect('/index/')