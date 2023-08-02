from django import forms

from .models import Post, Comment
from users.models import MyUser


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('objects', 'page_objects', 'is_published', 'author')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class UserForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'username',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
