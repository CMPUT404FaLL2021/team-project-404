# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from socialapp.forms import UserForm, PostForm, VisiChoices, CheckBox
from socialapp.models import *
import datetime

chosen_post = 5

# view of index.html
def index(request):
    users = User.objects.all()
    content = {'users': users}
    return render(request, "socialapp/index.html", content)

# view of mainPage
def mainPage(request):
    return render(request, "socialapp/mainPage.html")


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
                #response = redirect(show_post) # testing only, should set cookies go to main page
                #response.set_cookie('username', username)
                #return response 
                
                return render(request, 'socialapp/mainPage.html') # after test redict to the main page


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
            p = Post(post=post, username=username, visibility=visibility, unlisted=unlisted)
            p.save()
        return HttpResponse(p.post)

    else:
        form = PostForm()
        visibility = VisiChoices()
        check_box = CheckBox()

    return render(request, 'socialapp/add_post.html', {'form':form, 'visibility':visibility, 'check_box':check_box})     


# view of show_post.html
def show_post(request):
    post_to_show = Post.objects.get(pk=chosen_post)
    post_info = "Content: %s\n\nAuthor: %s\n\nDate: %s" % (post_to_show.post, post_to_show.username, post_to_show.date)
    #id_content = {'num':chosen_post}
    content = {'info':post_info}
    return render(request, 'socialapp/show_post.html', content)


# view of edit_post.html
def edit_post(request):
    p = Post.objects.get(pk=chosen_post)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            changed_post = form.cleaned_data['post']
            p.post = changed_post
            p.date = datetime.date.today()
            p.save()
            response = redirect(show_post)
            return response
    else:
        form = PostForm(initial={"post":p.post})
        #form.fields["post"].initial = p.post

    return render(request, 'socialapp/edit_post.html', {'form':form})


# view of logout.html
def logout(request):
    
    return redirect('/index/')