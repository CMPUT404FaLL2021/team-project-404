'''
this file we create the forms using the django.forms 
which is used in creating the forms in html pages
'''

from django import forms
from socialapp.models import *
from mdeditor . fields import MDTextFormField

#author form
class AuthorForm(forms.ModelForm):
    displayName = forms.CharField(label='displayName', required=True, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password'}), required=True)
    class Meta:
        model = Author
        fields = ('displayName', 'password')

#post form
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

    content = MDTextFormField()
    # content = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': hint_text}))
    visibility = forms.ChoiceField(label=False, choices = VISIBILITY_CHOICES, initial='PUBLIC')
    contentType = forms.ChoiceField(label=False, choices = CONTENT_TYPES, initial='PLAIN')
    class Meta:
        model = Post
        fields = ('content', 'description', 'title', 'unlisted', 'visibility', 'contentType')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title here'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
        }

#view form
class ViewerForm(forms.Form):
    viewer = forms.ChoiceField(label=False)

# class EditForm(forms.ModelForm):
#     edit = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': '...'}))
#     class Meta:
#         model = Post
#         fields = ('edit',)

#comment form
class CommentForm(forms.ModelForm):
    comment = forms.CharField(label=False, required=True, widget=forms.Textarea(attrs={'placeholder': 'Write a comment'}))
    class Meta:
        model = Comment
        fields = ('comment',)