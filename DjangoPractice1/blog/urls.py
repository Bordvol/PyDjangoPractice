from django.urls import path, re_path
from django.contrib import admin
from blog.views import (
    index_view,
    post_list_view,
    post_view,
)

app_name = 'blog'

urlpatterns = [
    path('index/', index_view, name='index'),
    path('', index_view, name='index'),
    path('posts/', post_list_view, name='post_list'),
    path('posts/<slug>', post_view, name='post'),
]
