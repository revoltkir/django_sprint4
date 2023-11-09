from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Location

admin.site.empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'text', 'post_image', 'image', 'category', 'location', 'pub_date', 'is_published']
    list_display = ('id', 'title', 'author', 'post_image', 'text_info', 'category',
                    'pub_date', 'location', 'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('text',)
    list_editable = ('category', 'is_published',)
    list_filter = ('created_at', 'is_published',)
    readonly_fields = ['post_image']
    list_per_page = 5
    ordering = ['-pub_date']
    save_on_top = True

    @admin.display(description="Краткое описание")
    def text_info(self, post: Post):
        return f'{post.text[:50]}...'

    @admin.display(description="Изображение")
    def post_image(self, post: Post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=50>")
        return 'Без картинки'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'slug',
                    'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
