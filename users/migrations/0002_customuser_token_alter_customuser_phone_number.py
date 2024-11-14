# Generated by Django 4.2.2 on 2024-11-13 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="token",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Token"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(
                blank=True,
                help_text="Введите номер телефона",
                max_length=50,
                null=True,
                verbose_name="Номер телефона",
            ),
        ),
    ]
