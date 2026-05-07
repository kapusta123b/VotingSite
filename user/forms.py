from dataclasses import fields
from importlib.metadata import files

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from django_recaptcha.fields import ReCaptchaField

from user.models import User


from allauth.account.forms import LoginForm, SignupForm

class UserLoginForm(LoginForm):
    captcha = ReCaptchaField()


class UserSignUpForm(SignupForm):
    captcha = ReCaptchaField()

class UserUpdateProfileForm(UserChangeForm):
    class Meta:
        model = User

        fields = (
            "username",
            "email",
        )
