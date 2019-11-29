from django.shortcuts import render
from blog import models as blog_models
from users import models as users_models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from blog.forms import AddPostForm, AddCommentForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

class PostListView(ListView):
    template_name = 'index.html'
    queryset = blog_models.post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_qs = blog_models.post.objects.all()

        paginator = Paginator(product_qs.order_by('-pk'), 5)
        page = self.request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        context['post_list'] = product_list
        context['total_posts_count'] = blog_models.post.objects.count()
        context['total_comments_count'] = blog_models.comment.objects.count()
        return context


class AddPostView(FormView):
    template_name = 'add_post.html'
    form_class = AddPostForm
    success_url = reverse_lazy('blog:index')
    user = get_user_model()

    def form_valid(self, form):
        obj = form.save(commit=False)

        user = self.request.user
        user_to_save = users_models.CustomUser()
        user_to_save.id = user.id
        obj.user_id = user_to_save


        obj.save()
        return super().form_valid(form)

class AddCommentView(FormView):
    form_class = AddCommentForm
    success_url = reverse_lazy('blog:index')
    user = get_user_model()

    def post(self, request, *args, **kwargs):
        print(request.POST.get("add_comment"))
        print(request.POST.get("pk"))

        comment = blog_models.comment()
        comment.message = request.POST.get("add_comment")

        pk  = request.POST.get("pk")
        post_to_save = get_object_or_404(blog_models.post, pk=pk)
        comment.post_id = post_to_save

        user_to_save = self.request.user
        comment.user_id = user_to_save

        comment.save()
        return redirect('blog:post' , pk)


def post_list_view(request):
    ctx = {}
    ctx['post_list'] = blog_models.post.objects.all()
    ctx['comments_list'] = {}
    ctx['total_posts_count'] = blog_models.post.objects.count()
    ctx['total_comments_count'] = blog_models.comment.objects.count()
    return render(request, 'index.html', ctx)


def post_view(request, pk):
    ctx = {}
    post = blog_models.post.objects.filter(pk=pk).first()
    if post:
        ctx['post'] = post
        ctx['comments_list'] = post.comment_post.all().order_by('-pk')
        ctx['comments_count'] = post.comment_post.all().count()
    return render(request, 'post.html', ctx)