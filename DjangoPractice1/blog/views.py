from django.shortcuts import render
from blog import models as blog_models


def index_view(request):
    ctx = {}
    ctx['post_list'] = blog_models.post.objects.all()[:5]
    ctx['total_count'] = blog_models.post.objects.count()
    return render(request, 'index.html', ctx)


def post_list_view(request):
    ctx = {}
    ctx['post_list'] = blog_models.post.objects.all()
    ctx['total_count'] = blog_models.post.objects.count()
    return render(request, 'index.html', ctx)


def post_view(request, slug):
    ctx = {}
    post = blog_models.post.objects.filter(slug=slug).first()
    if post:
        ctx['post'] = post
        ctx['comments_list'] = post.comment_post.all()
        ctx['comments_count'] = post.comment_post.all().count()
    return render(request, 'post.html', ctx)