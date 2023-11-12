from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now

from .forms import CommentForm, CreatePostForm
from .models import Post, Comment


def main_post_queryset():
    post_queryset = Post.objects.select_related(
        'author',
        'category',
        'location',
    ).filter(
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True,
    ).order_by("-pub_date")
    return post_queryset


def comments_main_post_queryset():
    post_queryset = (main_post_queryset()
                     .annotate(comment_count=Count("comments")))
    return post_queryset


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = "comment_id"


class ValidFormMixin:
    def __init__(self):
        self.request = None

    post_obj = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)


class PostEditMixin:
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'

    def __init__(self):
        self.request = None

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class DispatchMixin:
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs[self.pk_url_kwarg]})
