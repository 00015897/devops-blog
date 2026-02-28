from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Post


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

