from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Post, Location, Category, User, Comment


class CreatePostForm(forms.ModelForm):
    """Форма создания и редактирования публикации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана',
                                      label='Категории')
    location = forms.ModelChoiceField(queryset=Location.objects.all(),
                                      required=False,
                                      empty_label='Местоположение не выбрано',
                                      label='Местоположение')

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']

        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


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
