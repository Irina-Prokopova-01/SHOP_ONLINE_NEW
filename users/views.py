from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
import secrets
from .forms import CustomUserCreationForm
from .models import CustomUser
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Укажите имя URL для страницы логина

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

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
    return redirect(reverse_lazy('login'))

