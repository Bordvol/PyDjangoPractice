from django import forms
from users.models import CustomUser

from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('nickname', 'name', 'surname', 'email', 'phone', 'password1', 'password2')
