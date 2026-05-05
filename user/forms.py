from dataclasses import fields
from importlib.metadata import files

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from django_recaptcha.fields import ReCaptchaField


from user.models import User


class UserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegistrationForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateProfileForm(UserChangeForm):
    class Meta:
        model = User

        fields = (
            "username",
            "email",
        )
