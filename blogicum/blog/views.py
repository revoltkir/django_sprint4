from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (DetailView, ListView,
                                  CreateView, UpdateView, DeleteView)

from .forms import CreatePostForm, ProfileUserForm, CommentForm
from .models import Category, Post, User
from .utils import (main_post_queryset, comments_main_post_queryset,
                    CommentMixin, ValidFormMixin, PostEditMixin)


class MainPagePostListView(ListView):
    """Список публикаций на главной странице."""

    template_name = 'blog/index.html'
    paginate_by = settings.PUBLICATIONS_NUMBER

    def get_queryset(self):
        return comments_main_post_queryset()


class PostDetailView(DetailView):
    """Страница выбранной публикации."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    post = None

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.post.author != self.request.user:
            if not (self.post.is_published and self.post.category.is_published
                    and self.post.pub_date <= timezone.now()):
                raise Http404('Публикация не найдена')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryPostListView(ListView):
    """Страница со списком публикаций выбранной категории."""

    template_name = 'blog/category.html'
    paginate_by = settings.PUBLICATIONS_NUMBER

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        return context

    def get_queryset(self):
        return (main_post_queryset()
                .filter(category__slug=self.kwargs['category_slug']))


class PostCreateView(LoginRequiredMixin, PostEditMixin,
                     ValidFormMixin, CreateView):
    """Создание публикации."""


class PostUpdateView(LoginRequiredMixin, PostEditMixin, UpdateView):
    """Редактирование публикации."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, PostEditMixin, DeleteView):
    """Удаление публикации."""

    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreatePostForm(instance=self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)


class ProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    """Профиль пользователя."""

    form_class = ProfileUserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class ProfileUserListView(ListView):
    """Список постов пользователя."""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = settings.PUBLICATIONS_NUMBER
    author = None

    def get_queryset(self):
        username = self.kwargs['username']
        self.author = get_object_or_404(User, username=username)
        if self.author == self.request.user:
            queryset = Post.objects.filter(author=self.author)
        else:
            queryset = (super().get_queryset()
                        .filter(author=self.author))
        return (queryset.annotate(comment_count=Count('comments'))
                .order_by("-pub_date"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        context['user'] = self.request.user
        return context


class CommentCreateView(LoginRequiredMixin, ValidFormMixin,
                        CommentMixin, CreateView):
    """Создание комментария."""

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail',
                            self.kwargs['post_id'])
        get_object_or_404(main_post_queryset()
                          .filter(pk=self.kwargs[self.pk_url_kwarg]))
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})
