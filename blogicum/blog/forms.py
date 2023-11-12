from django import forms
from django.utils import timezone

from .models import Post, User, Comment


class CreatePostForm(forms.ModelForm):
    """Форма создания и редактирования публикации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']

        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['location'].empty_label = "Местоположение не выбрано"


class ProfileUserForm(forms.ModelForm):
    """Форма профиля"""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CommentForm(forms.ModelForm):
    """Форма комментария"""

    class Meta:
        model = Comment
        fields = ('text',)
