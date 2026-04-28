from dataclasses import fields
from importlib.metadata import files

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from user.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegistrationForm(UserCreationForm):

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
