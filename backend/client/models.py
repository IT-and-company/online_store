from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class City(models.Model):
    name = models.CharField(
        'Название города',
        max_length=settings.MAX_LENGTH_3
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200,
        blank=False,
        help_text='Введите своё имя'
    )
    phone = PhoneNumberField(
        'Телефон',
        null=False,
        blank=False,
        help_text='Введите номер телефона'
    )
    email = models.EmailField(
        'Email',
        blank=False,
        help_text='Введите ваш email'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Город доставки'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
