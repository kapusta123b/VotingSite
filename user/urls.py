from django.urls import path

from allauth.account.views import LoginView, SignupView, LogoutView, PasswordChangeView
from user import views

app_name = 'user'

urlpatterns = [
    path('profile/<int:user_id>/', views.ProfileUser.as_view(), name='profile'),
    path('profile/update/<int:user_id>/', views.UpdateUserInformationView.as_view(), name='update'),

    path('login/', LoginView.as_view(), name='login'),
    path('registration/', SignupView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change/', PasswordChangeView.as_view(), name='change'),
]