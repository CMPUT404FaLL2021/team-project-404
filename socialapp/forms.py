from django import forms

from socialapp.models import *

class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', required=True)
    password = forms.CharField(label='password', widget=forms.PasswordInput(), required=True)
    class Meta:
        model = User
        fields = ('username', 'password')

class PostForm(forms.ModelForm):
    post = forms.CharField(label=False, required=True, widget=forms.TextInput(attrs={'placeholder': 'Write a caption ...'}))
    class Meta:
        model = Post
        fields = ('post',)

class CheckBox(forms.Form):
    friends_only = forms.BooleanField(label='friends_only', required=False)
    class Meta:
        model = Post