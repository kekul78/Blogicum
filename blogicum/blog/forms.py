from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment
from users.models import MyUser
User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        # Указываем, что надо отобразить все поля.
        exclude = ('objects', 'page_objects', 'is_published', 'author')

        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class UserForm(forms.ModelForm):

    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = MyUser

        fields = ('first_name', 'last_name', 'email', 'username',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
