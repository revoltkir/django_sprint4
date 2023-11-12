from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Location, Comment

admin.site.empty_value_display = '-пусто-'

NUMBER_OF_SIGNS = 50


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Публикации."""

    fields = [
        'title', 'author', 'text', 'post_image',
        'image', 'category', 'location', 'pub_date',
        'is_published',
    ]
    list_display = (
        'id', 'title', 'author', 'post_image',
        'text_info', 'category', 'pub_date', 'location',
        'is_published', 'created_at', 'comment_count',
    )
    list_display_links = ('title',)
    search_fields = ('text', 'title')
    list_editable = ('category', 'is_published',)
    list_filter = ('created_at', 'is_published', 'category', 'author')
    readonly_fields = ['post_image']
    list_per_page = 10
    ordering = ['-pub_date']
    save_on_top = True

    @admin.display(description="Краткое описание")
    def text_info(self, post: Post):
        return f'{post.text[:NUMBER_OF_SIGNS]}...'

    @admin.display(description="Изображение")
    def post_image(self, post: Post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=50>")
        return 'Без картинки'

    @admin.display(description="Комментарии")
    def comment_count(self, comment):
        count_comment = comment.comments.count()
        return 'No comments' if count_comment <= 0 else count_comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории."""

    list_display = ('id', 'title', 'description', 'slug',
                    'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Местоположение."""

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'post', 'author',
    )
    list_display_links = ('author',)
