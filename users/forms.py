from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Введите номер телефона"
    )
    country = forms.CharField(
        max_length=50, required=False, help_text="Укажите Вашу страну проживания"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            "email",
            "phone_number",
            "avatar",
            "country",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["avatar"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите Ваш аватар"}
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите Вашу страну проживания"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_number