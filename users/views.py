# from audioop import reverse
# from urllib import request

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
import secrets
# from django.conf import settings
# from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:product_list')  # Укажите имя URL для страницы логина


    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     self.send_welcome_email(user.email)
    #     return super().form_valid(form)
    #
    #
    # def send_welcome_email(self, user_email):
    #     subject = "Добро пожаловать!"
    #     message = "Спасибо, что зарегистрировались в нашем магазине!"
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [user_email]
    #     send_mail(subject, message, email_from, recipient_list)


    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        # url = f'http://{host}/{reverse('email-confirm', args=[token])}/'
        url = self.request.build_absolute_uri(reverse_lazy('users:email-confirm', args=[token]))

        send_mail(
            subject='Подтверждение почты',
            message=f'Привет. Перейди по ссылке для подтверждения почты {url}.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        # Вывод ошибок формы в консоль для отладки
        print("Форма не валидна:", form.errors)

        # Вы можете также добавить дополнительную логику здесь,
        # например, вернуть сообщение об ошибке пользователю.

        # Возвращаем стандартный ответ для невалидной формы
        return super().form_invalid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:login'))

