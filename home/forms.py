from dataclasses import field, fields
from django.forms import ModelForm
from .models import Post, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host','participants']



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']
