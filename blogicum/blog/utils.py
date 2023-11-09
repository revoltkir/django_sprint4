from django.utils.timezone import now

from .models import Post


def main_post_queryset():
    post_queryset = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True,
    )
    return post_queryset
