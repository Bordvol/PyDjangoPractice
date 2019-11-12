from django.db import models
from django.conf import settings
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Post''s owner', on_delete=models.PROTECT, null=True, related_name='post_user')
    title = models.CharField('Post title', max_length=255, blank=False, unique=True)
    slug = AutoSlugField(populate_from='title',unique=True, null=True)
    image = models.ImageField(verbose_name='Picture',upload_to='post',null=True,blank=True)
    short_description = models.CharField('Post short description', max_length=255, blank=False)
    message = models.CharField('Message', max_length=4000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.title}, {self.short_description}'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def get_comments_count(self):
       return self.comment_post.all().count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

		
class comment(models.Model):
    post_id = models.ForeignKey(post, verbose_name='Post', on_delete=models.CASCADE, null=True, related_name='comment_post')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Comment''s user', on_delete=models.PROTECT, null=True, related_name='comment_user')
    user_name = models.CharField('User name', max_length=255, blank=False, unique=False)
    message = models.CharField('Message', max_length=4000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.post_id}, {self.message}, '

    def get_absolute_url(self):
        return reverse('blog:comment', kwargs={'pk': self.pk})