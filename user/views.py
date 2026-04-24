from django.urls import reverse_lazy

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView

from user.forms import UserLoginForm, UserRegistrationForm
from user.models import User

class RegisterUser(CreateView):
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user:login')



class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')



class ProfileUser(DetailView):
    template_name = 'user/profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'
    model = User