from django.urls import path, re_path
from django.contrib import admin
from blog.views import (
    post_list_view,
    post_view,
    PostListView,
    AddPostView,
    AddCommentView,
)

app_name = 'blog'

urlpatterns = [
    path('index/', PostListView.as_view(), name='index'),
    path('', PostListView.as_view(), name='index'),
    path('posts/', post_list_view, name='all_posts'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('posts/<pk>', post_view, name='post'),
]
