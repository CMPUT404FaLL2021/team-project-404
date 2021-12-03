'''
this file we create the functions and achieve rerender function.
views.py includes all the function of the pages
'''
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from requests.auth import HTTPBasicAuth
import json
import uuid
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from socialapp.forms import AuthorForm, PostForm, CommentForm, ViewerForm
from socialapp.models import *
from django.urls import reverse
from django.utils import timezone
from socialapp.api.serializers import *

remote_nodes = ["https://cmput404fall21g11.herokuapp.com/", "https://fast-chamber-90421.herokuapp.com/", "https://social-dis.herokuapp.com/"]
credentials = [('team13', '123456'), ('defaul', 'default'), ('socialdistribution_t03', 'c404t03')]


# view of index.html
def index(request):
    authors = Author.objects.all()
    content = {'authors': authors}
    return render(request, "socialapp/index.html", content)

# view of main_page
def main_page(request, author_id):
    try:
        Author.objects.get(pk=author_id)
    except:
        return HttpResponseNotFound('404 Page Not Found, author %s does not exist' %(author_id))
    
    p_list = Post.objects.filter(visibility='PUBLIC').order_by('-published')
    remote_post = []

    # get posts from team11
    api_url1 = remote_nodes[0] + 'api/posts/'
    content_get1 = requests.get(api_url1, auth=credentials[0])
    if content_get1.status_code == 200:
        for post in content_get1.json()['items']:
            if post['visibility'] == 1:
                # post['url'] = post['id']
                post['author']['id'] = uuid.UUID(post['author']['id'].split('/')[-2])
                post['id'] = uuid.UUID(post['id'])
                remote_post.append(post)
    
    # get posts from team09
    # team 09 does not require auth at the time
    api_url2_1 = remote_nodes[1] + 'authors?page=1&size=100/'
    content_get2_1 = requests.get(api_url2_1)
    if content_get2_1.status_code == 200:
        for remote_author in content_get2_1.json()['items']:
            content_get2_2 = requests.get(remote_author['id']+'/posts/')
            if content_get2_2.status_code == 200:
                for post in content_get2_2.json():
                    if post['visibility'] == 'PUBLIC':
                        post['url'] = post['id']
                        post['author']['id'] = uuid.UUID(post['author']['id'].split('/')[-1])
                        post['id'] = uuid.UUID(post['id'].split('/')[-1])
                        remote_post.append(post)
    
    # get posts from team03
    api_url3 = remote_nodes[2] + 'posts/'
    content_get3 = requests.get(api_url3, auth=credentials[2])
    if content_get3.status_code == 200:
        for post in content_get3.json()['items']:
            if post['visibility'] == 'PUBLIC':
                post['url'] = post['id']
                post['author']['id'] = uuid.UUID(post['author']['id'].split('/')[-1])
                post['id'] = uuid.UUID(post['id'].split('/')[-1])
                remote_post.append(post)

    return render(request, "socialapp/main_page.html", {'author_id':author_id, 'p_list':p_list, 'remote_post':remote_post})


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
            
            messages.success(request, 'Sign up successfully!')
            author = Author.objects.get(displayName=name)
            author.url = author.url + str(author.id)
            author.save()
            inbox = Inbox(author=author)
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
def author_inbox(request, author_id):
    author = Author.objects.get(pk=author_id)
    inbox = Inbox.objects.get(author=author)
    friend_request_list = FriendRequest.objects.filter(inbox=inbox)
    posts = Post.objects.filter(inbox=inbox)
    author_posts = Post.objects.filter(author=author)
    likes = Like.objects.filter(inbox=inbox).order_by('-id')
    comments = Comment.objects.filter(inbox=inbox).order_by('-published')

    if request.method == 'POST':
        for friend_request in friend_request_list:
            if 'follow_button_' + friend_request.actor.displayName in request.POST:
                friend_request.actor.followers.add(author)
                # wthether send friend request
                if friend_request.actor not in author.followers.all():
                    new_friend_request = FriendRequest(actor=author, object=friend_request.actor, inbox=Inbox.objects.get(author=friend_request.actor))
                    new_friend_request.save()
                friend_request.delete()
                return redirect(author_inbox, author_id)

    return render(request, 'socialapp/author_inbox.html', {'author_id': author_id, 'friend_request_list': friend_request_list, 'posts':posts, 'likes':likes, 'comments':comments})


# view of author_profile.html
def author_profile(request, author_id):
    if request.method == 'GET':
        me = Author.objects.get(pk=author_id)
        p_list = Post.objects.filter(author=me, unlisted=False).order_by('-published')

    return render(request, "socialapp/author_profile.html", {'author': me, 'p_list': p_list})


def edit_profile(request, author_id):
    me = Author.objects.get(pk=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            if 'avatar' in request.FILES:
                changed_avatar = form.cleaned_data["avatar"]
                me.avatar = changed_avatar
            changed_name = form.cleaned_data['displayName']
            changed_passwaord = form.cleaned_data['password']
            me.displayName = changed_name
            me.password = changed_passwaord
            #me.avatar = changed_avatar
            me.save()
            response = redirect(author_profile, author_id)
            return response
    else:
        form = AuthorForm(initial={"displayName":me.displayName, "password":me.password})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_profile.html', {'form':form, 'author_id':author_id})


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
                viewerForm = ViewerForm()
                viewers_choices = [(v.id, v.displayName) for v in Author.objects.all()]
                viewerForm.fields['viewer'].choices = viewers_choices
                return render(request, 'socialapp/select_viewers.html', {'form':viewerForm, 'author_id':author_id, 'post_id':p.id})

            response = redirect(main_page, author_id)
            return response

    else:
        form = PostForm()

    return render(request, 'socialapp/add_post.html', {'form':form, 'author_id':author_id})  

def select_viewers(request, author_id, post_id):
    viewers_choices = [(v.id, v.displayName) for v in Author.objects.all()]
    if request.method == 'POST':
        form = ViewerForm()
        form.fields['viewer'].choices = viewers_choices
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
        form.fields['viewer'].choices = viewers_choices

    return render(request, 'socialapp/select_viewers.html', {'form':form, 'author_id':author_id, 'post_id':post_id})


# helper function for checking if I like the post
def if_like(remote, post_to_show, author_id, post_url):
    if remote:
        like_url = post_url + 'likes'
        try:
            likes = requests.get(like_url, auth=('team13', '123456')).json()
        except:
            return False, 0
        for like in likes['items']:
            author = like['author']
            if isinstance(author, str):
                author = json.loads(like['author'])
            if str(author['id']) == str(author_id) or str(author['uuid']) == str(author_id):
                return True, len(likes['items'])
        return False, len(likes['items'])
    else:
        if post_to_show.likes.filter(id=author_id).exists():
            return True, post_to_show.like_count
        return False, post_to_show.like_count

# helper function for checking the follow status
def follow_check(post_to_show, author_id, if_remote):
    if_follow = False
    if_follows_me = False

    if not if_remote:
        post_author = post_to_show.author
        me = Author.objects.get(pk=author_id)

        if me in post_author.followers.all():
            if_follow = True
        if post_author in me.followers.all():
            if_follows_me = True
        return if_follow, if_follows_me
    
    else:
        remote_post_author = post_to_show['author']
        me = Author.objects.get(pk=author_id)
        if remote_post_author in me.followers.all():
            if_follows_me = True
    
    # # subject to change, just assumptions
    # if remote_post_author['host'] == "https://cmput404fall21g11.herokuapp.com/":
    #     if_follow = requests.get(remote_nodes[0]+"api/author/"+remote_post_author.id+"/followers/"+me.id, auth=credentials[0])
    # elif remote_post_author['host'] == "https://fast-chamber-90421.herokuapp.com/":
    #     if_follow = requests.get(remote_nodes[1]+"author/"+remote_post_author.id+"/followers/"+me.id, auth=credentials[1])
    # elif remote_post_author['host'] == "https://social-dis.herokuapp.com/":
    #     if_follow = requests.get(remote_nodes[1]+"author/"+remote_post_author.id+"/followers/"+me.id, auth=credentials[2])
    
    return if_follow, if_follows_me


def get_remote_comments(post_url):
    comments_url = post_url + 'comments/'
    get_comments = requests.get(comments_url, auth=credentials[0])
    if get_comments.status_code == 200:
        post_comments = get_comments.json()["items"]
        comment_count = len(post_comments)
    else:
        post_comments = None
        comment_count = 0
    return post_comments, comment_count

def get_request_author(author_id):
    request_author = {}
    author =Author.objects.get(id=author_id)
    request_author['uuid'] = str(author.id)
    request_author['id'] = author.url
    request_author['url'] = author.url
    request_author['displayName'] = author.displayName
    request_author['host'] = author.host
    return json.dumps(request_author)

# view of show_post.html
def show_post(request, author_id, show_post_id):
    REMOTE = False
    post_url = None
    try:
        post_url = request.GET['remote_post_url']
        REMOTE = True
        credential = None
        
        # credentials might be different!!!!!!
        # 之后应该要加if判断是哪个remote node然后用相应的credential进行判断
        if "https://cmput404fall21g11.herokuapp.com/" in post_url:
            credential = credentials[0]
        elif "https://fast-chamber-90421.herokuapp.com/" in post_url:
            credential = credentials[1]
        # ???? 为啥这第三组http和https混着用😵‍💫
        elif "http://social-dis.herokuapp.com/" in post_url:
            credential = credentials[2]

        get_post = requests.get(post_url, auth=credential)
        if get_post.status_code == 200:
            post_to_show = get_post.json()
            post_to_show['id'] = show_post_id
        else:
            return HttpResponseNotFound('404 Page Not Found (view.py show_post 1st) %s  -- %s\n%s' %(author_id, show_post_id, post_url))
    except:
        post_to_show = Post.objects.get(pk=show_post_id)

    context = {'post_to_show': post_to_show, 'author_id': author_id, 'post_comments':None, 'comment_count':0, 'post_url':post_url}
    like_status, like_count = if_like(REMOTE, post_to_show, author_id, post_url)
    context['like_status'] = like_status
    context['like_count'] = like_count

    follow_status, friend_request_status = follow_check(post_to_show, author_id, REMOTE)
    context['follow_status'] = follow_status

    if request.method == 'GET':
        if REMOTE:
            post_comments, comment_count = get_remote_comments(post_url)
        else:
            post_comments = Comment.objects.filter(post=post_to_show).order_by("-published")
            comment_count = post_comments.count()
        
        if post_comments:
            context['post_comments'] = post_comments
            context['comment_count'] = comment_count

        if 'delete_button' in request.GET:
            post_to_show.delete()
            response = redirect(main_page, author_id)
            return response


    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        context['form'] = form
        if 'like_button' in request.POST:
            if like_status:
                if REMOTE:
                    data = {}
                    data['type'] = 'like'
                    data['author'] = get_request_author(author_id)
                    data['object'] = post_to_show['id']
                    request_url = post_url + 'likes'
                    print('test: '+data+'\nurl: '+request_url)
                else:
                    post_to_show.likes.remove(Author.objects.get(id=author_id))
                    l = Like.objects.get(author=Author.objects.get(id=author_id), object=post_to_show)
                    l.delete()
            else:
                if REMOTE:
                    data = {
                        "type" :"like",
                        "author" : get_request_author(author_id),
                        "object" : post_url
                    }
                    request_url = post_to_show["author"]["id"] + "inbox/"
                    r = requests.post(request_url, data=data, auth=HTTPBasicAuth("team13", "123456"), headers={"Content-Type":"application/json"})
                    print(data)
                    print(json.dumps(data))
                else:
                    post_to_show.likes.add(Author.objects.get(id=author_id))
                    l = Like(author=Author.objects.get(id=author_id), object=post_to_show, inbox=Inbox.objects.get(author=post_to_show.author))
                    l.save()

        elif 'post_button' in request.POST:
            comment = form.data['comment']
            if form.is_valid():
                comment = form.cleaned_data['comment']
                if REMOTE:
                    request_author = get_request_author(author_id)
                    data = {}
                    data['type'] = 'comment'
                    data['author'] = request_author
                    data['commnet'] = comment
                    data['contentType'] = 'text/plain'
                    print(data)
                else:
                    c = Comment(comment=comment, post=post_to_show, author=Author.objects.get(id=author_id), inbox=Inbox.objects.get(author=post_to_show.author))
                    c.save()
        
        elif 'delete_comment' in request.POST:
            comment_id = request.POST['delete_comment']
            del_comment = Comment.objects.get(id=comment_id)
            del_comment.delete()

        elif 'share_post' in request.POST:
            if not REMOTE:
                author = Author.objects.get(id=author_id)
                content = post_to_show.content + ("\n(%s forwarded %s's post)" % (author.displayName, post_to_show.author.displayName))
                p = Post(title=post_to_show.title, description=post_to_show.description, content=content, author=Author.objects.get(id=author_id))
                p.save()
                response = redirect(main_page, author_id)
                return response
            else:
                author = Author.objects.get(id=author_id)
                content = post_to_show['content'] + ("\n(%s forwarded %s's post)" % (author.displayName, post_to_show['author']['displayName']))
                p = Post(title=post_to_show['title'], description=post_to_show['description'], content=content, author=Author.objects.get(id=author_id), origin=post_to_show['origin'])
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
                if not friend_request_status:
                    friend_request = FriendRequest(actor=me, object=post_author, inbox=Inbox.objects.get(author=post_author))
                    friend_request.save()
        if REMOTE:
            return HttpResponseRedirect(reverse('show_post', args=[author_id, show_post_id]) + '?remote_post_url=' + post_url)
        else:
            return HttpResponseRedirect(reverse('show_post', args=[author_id, show_post_id]))


    else:
        form = CommentForm()

    context['form'] = form
    context['if_remote'] = 0
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