from django import forms
from .models import Product
from django.core.exceptions import ValidationError

forbidden_words = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'first_name'
        self.fields["title"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Введите наименование продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'last_name'
        self.fields["description"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Введите описание продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'year'
        self.fields["image"].widget.attrs.update({
            "class": "form-control",  # Добавление CSS-класса для стилизации поля
            "placeholder": 'Укажите изображение продукта'
        })

        # Настройка атрибутов виджета для поля 'email'
        self.fields["category"].widget.attrs.update({
            "class": "form-control",
            "placeholder": 'Укажите категорию продукта'
        })

        self.fields["price"].widget.attrs.update({
            "class": "form-control",
            "placeholder": 'Укажите цену продукта'
        })

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if any(word in title.lower() for word in forbidden_words):
            raise ValidationError("В наименовании есть запрещенные слова.")
        elif Product.objects.filter(title=title).exists():
            raise ValidationError("Продукт с таким наименованием уже есть.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if any(word in description.lower() for word in forbidden_words):
            raise ValidationError("В наименовании есть запрещенные слова.")
        return description