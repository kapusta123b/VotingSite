from django.urls import path

from django.contrib.auth.views import LogoutView

from user import views

app_name = 'user'

urlpatterns = [
    path('profile/<int:user_id>', views.ProfileUser.as_view(), name='profile'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('registration/', views.RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]