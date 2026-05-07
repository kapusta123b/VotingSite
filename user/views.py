from django.urls import reverse

from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from user.forms import UserUpdateProfileForm
from user.models import User


class ProfileUser(DetailView):
    template_name = "user/profile.html"
    context_object_name = "profile_user"
    pk_url_kwarg = "user_id"
    model = User


from django.contrib import messages
from allauth.account.models import EmailAddress

class UpdateUserInformationView(UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    pk_url_kwarg = "user_id"
    template_name = "user/profile.html"
    context_object_name = "profile_user"

    def form_valid(self, form):
        old_email = User.objects.get(pk=self.object.pk).email
        new_email = form.cleaned_data.get('email')

        if new_email and new_email != old_email:
            email_address, created = EmailAddress.objects.get_or_create(
                user=self.request.user, 
                email=new_email
            )
            email_address.verified = False
            email_address.save()
            
            # Отправляем подтверждение через метод модели
            email_address.send_confirmation(self.request, signup=False)
            
            messages.info(self.request, f"Confirmation email sent to {new_email}. Please verify it to complete the change.")
            
            form.cleaned_data['email'] = old_email
            form.instance.email = old_email

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user:profile", kwargs={"user_id": self.object.pk})

