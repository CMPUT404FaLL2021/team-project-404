from django import forms

from socialapp.models import *

class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', required=True)
    password = forms.CharField(label='password', widget=forms.PasswordInput(), required=True)
    class Meta:
        model = User
        fields = ('username', 'password')

class PostForm(forms.ModelForm):
    post = forms.CharField(label='post', required=True)
    class Meta:
        model = Post
        fields = ('post',)