from django.db import models

from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Название", help_text="Введите название категории"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание категории",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["title"]


class Product(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Название", help_text="Введите название продукта"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание продукта",
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите фотографию продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    publish_status = models.BooleanField(
        default=False,
        help_text="Укажите статус публикации продукта",
        verbose_name="Статус публикации",
    )
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену продукта")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")
    view_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0,
        help_text="Укажите кол-во просмотров",
    )

    def __str__(self):
        return f"{self.title} {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["title"]
        permissions = [
            ("can_unpublish_product", "can unpublish product"),
        ]
