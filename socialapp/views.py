# Create your views here.
from django.shortcuts import render, redirect
from socialapp.forms import UserForm
from socialapp.models import *
from django.http import HttpResponse

def index(request):
    users = User.objects.all()
    content = {'users': users}
    return render(request, "index.html", content)

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            info = 'Sign Up Successfully!'
            content = {'info':info}
            return render(request, 'index.html', content)
            #return HttpResponse('Sign Up Successfully!')
        else:
            info = 'Sign Up Failed!'
            content = {'info':info}
            return render(request, 'index.html', content)
            #return HttpResponse(form.errors)
    else:
        form = UserForm()
    return render(request, 'register.html', {'form':form})

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
                return render(request, 'index.html', content)
            else:
                info = 'Login Failed!'
                content = {'info':info}
                return render(request, 'index.html', content)
    else:
        form = UserForm()
    
    return render(request, 'login.html', {'form':form})

def logout(request):
    
    return redirect('/index/')