from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class BackCallOrder(models.Model):
    name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_1,
        blank=False,
        help_text='Введите своё имя'
    )
    phone = PhoneNumberField(
        'Телефон',
        null=False,
        blank=False,
        region='RU',
        max_length=settings.MAX_LENGTH_3,
        help_text='Введите номер телефона'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Order(BackCallOrder):
    email = models.EmailField(
        'Email',
        blank=False,
        help_text='Введите ваш email'
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=settings.MAX_LENGTH_1
    )

    class Meta:
        ordering = ('phone',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class BackCall(BackCallOrder):
    class Meta:
        ordering = ('phone',)
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратные звонки'
