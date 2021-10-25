from django import forms

from socialapp.models import *

class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', required=True, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password'}), required=True)
    class Meta:
        model = User
        fields = ('username', 'password')

class PostForm(forms.ModelForm):
    CONTENT_TYPES = {
        ("MARKDOWN", 'text/markdown'),
        ("PLAIN", 'text/plain')
        # add png & jpeg
    }
    VISIBILITY_CHOICES = {
        ("PUBLIC", 'public'),
        ("FRIENDS", 'friends only'),
        ("PRIVATE", 'private')
    }
    hint_text = "Write a caption ..."

    post = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': hint_text}))
    visibility = forms.ChoiceField(label=False, choices = VISIBILITY_CHOICES, initial='PUBLIC')
    content_type = forms.ChoiceField(label=False, choices = CONTENT_TYPES, initial='PLAIN')
    class Meta:
        model = Post
        fields = ('post', 'description', 'title', 'unlisted', 'visibility', 'content_type')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title here'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
        }

# class EditForm(forms.ModelForm):
#     edit = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': '...'}))
#     class Meta:
#         model = Post
#         fields = ('edit',)


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': 'Write a comment'}))
    class Meta:
        model = Comment
        fields = ('comment',)