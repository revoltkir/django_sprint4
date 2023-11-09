from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, CreateView

from .models import Category, Post
from .utils import main_post_queryset


# def index(request):
#     posts = main_post_queryset()[:settings.PUBLICATIONS_NUMBER]
#     context = {'post_list': posts}
#     return render(request, 'blog/index.html', context)


# def post_detail(request, id):
#     posts = get_object_or_404(main_post_queryset(), pk=id)
#     context = {'post': posts}
#     return render(request, 'blog/detail.html', context)
#
class IndexView(ListView):
    template_name = 'blog/index.html'
    paginate_by = settings.PUBLICATIONS_NUMBER
    allow_empty = False

    def get_queryset(self):
        return main_post_queryset()


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(main_post_queryset(), pk=self.kwargs['id'])


# def category_posts(request, category_slug):
#     category = get_object_or_404(
#         Category,
#         slug=category_slug,
#         is_published=True
#     )
#     posts = main_post_queryset().filter(category=category, )
#     context = {'post_list': posts, 'category': category}
#     return render(request, 'blog/category.html', context)


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    paginate_by = settings.PUBLICATIONS_NUMBER
    # context_object_name = 'post_list'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        context['title'] = category.title
        context['description'] = category.description
        return context

    def get_queryset(self):
        return main_post_queryset().filter(category__slug=self.kwargs['category_slug'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category = context['post_list'][0].category
    #     context['title'] = category.title
    #     context['description'] = category.description
    #
    #     return context


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
