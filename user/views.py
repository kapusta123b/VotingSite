from django.urls import reverse, reverse_lazy

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView

from user.forms import UserLoginForm, UserRegistrationForm, UserUpdateProfileForm
from user.models import User


class RegisterUser(CreateView):
    form_class = UserRegistrationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("user:login")


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = "user/login.html"

    def get_success_url(self):
        return reverse_lazy("main:index")


class ProfileUser(DetailView):
    template_name = "user/profile.html"
    context_object_name = "profile_user"
    pk_url_kwarg = "user_id"
    model = User


class UpdateUserInformationView(UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    pk_url_kwarg = "user_id"
    template_name = "user/profile.html"
    context_object_name = "profile_user"

    def get_success_url(self):
        return reverse("user:profile", kwargs={"user_id": self.object.pk})
