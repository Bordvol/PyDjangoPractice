from django import forms
from blog.models import post, comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('title', 'short_description', 'message', 'image')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('message',)
