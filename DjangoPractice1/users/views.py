from django.views.generic import TemplateView, FormView, RedirectView, ListView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.forms import RegisterForm
from django.http import JsonResponse
from blog import models as blog_models


class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    form_class = UserChangeForm
    queryset = blog_models.post.objects.all()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post_list'] = blog_models.post.objects.filter(user_id=self.request.user).all().order_by('-pk')
        ctx['comments_list'] = blog_models.comment.objects.exclude(user_id=self.request.user).all().order_by('-pk')
        ctx['total_posts_count'] = blog_models.post.objects.filter(user_id=self.request.user).count()
        ctx['total_comments_count'] = blog_models.comment.objects.filter(user_id=self.request.user).count()
        return ctx

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.save()
        user.send_user_mail('Registration', 'Welcome!')
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'blog:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
