from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # path('', index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('posts/<int:id>/', post_detail, name='post_detail'),
    path('posts/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('category/<slug:category_slug>/',category_posts, name='category_posts'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),

]
