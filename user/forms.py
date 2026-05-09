from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError

from django_recaptcha.fields import ReCaptchaField

from user.models import User


from allauth.account.forms import LoginForm, SignupForm

class UserLoginForm(LoginForm):
    captcha = ReCaptchaField()


class UserSignUpForm(SignupForm):
    captcha = ReCaptchaField()

class UserUpdateProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already taken.")
        
        return username
