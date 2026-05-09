from django.urls import reverse

from django.contrib import messages

from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from user.forms import UserUpdateProfileForm
from user.models import User

from allauth.account.models import EmailAddress

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

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if 'username' in form.changed_data:
            messages.success(self.request, "Username updated successfully.")

        if 'email' in form.changed_data:
            new_email = form.cleaned_data.get('email')

            email_address, _ = EmailAddress.objects.get_or_create(
                user=self.request.user, 
                email=new_email
            )
            email_address.verified = False
            email_address.save()
            email_address.send_confirmation(self.request, signup=False)
            
            messages.info(self.request, f"Confirmation email sent to {new_email}. Please verify it.")
            
        return response

    def form_invalid(self, form):
        messages.error(self.request, "This username is already taken. Please choose a different one.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("user:profile", kwargs={"user_id": self.object.pk})


