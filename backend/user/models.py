from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email', 'address']

    phone = PhoneNumberField(
        'phone',
        null=False,
        blank=False,
        unique=True,
        help_text='Введите ваш телефон'
    )

    class Meta:
        ordering = ('phone',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone

