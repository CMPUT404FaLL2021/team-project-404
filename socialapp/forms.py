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

# reference: https://www.geeksforgeeks.org/choicefield-django-forms/
class VisiChoices(forms.Form):
    VISIBILITY_CHOICES = {
        ("PUBLIC", 'public'),
        ("FRIENDS", 'friends only'),
        ("PRIVATE", 'private')
    }
    visibility = forms.ChoiceField(choices = VISIBILITY_CHOICES)
    class Meta:
        model = Post
        fields = ('visibility',)

class CheckBox(forms.Form):
    check_box = forms.BooleanField(required=False, label=False)
    class Meta:
        model = Post