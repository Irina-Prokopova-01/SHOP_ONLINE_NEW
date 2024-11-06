from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "publication_sign", "image", "text"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'first_name'
        self.fields["title"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Введите наименование поста'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'last_name'
        self.fields["text"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Введите описание текст'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'year'
        self.fields["image"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Укажите изображение поста'
        })

        # Настройка атрибутов виджета для поля 'email'
        self.fields["publication_sign"].widget.attrs.update({
            "class": "form-control"
        })

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if Post.objects.filter(title=title).exists():
            raise ValidationError(
                "Пост с таким наименование уже есть."
            )
        return title