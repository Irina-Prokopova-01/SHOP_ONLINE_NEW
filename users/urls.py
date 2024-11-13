from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserCreateView, email_verification
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:product_list'), name='logout'),
    path('register/', UserCreateView.as_view(template_name="users/register.html"), name='register'),
    path('email-confirm/<str:token>', email_verification, name='email-confirm')
]