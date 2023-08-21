from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    phone = PhoneNumberField(
        'Номер телефона',
        null=True,
        blank=True,
        unique=True,
        help_text='Введите ваш телефон'
    )
    email = models.EmailField(
        'Электронная почта',
        null=False,
        blank=False,
        unique=True,
        max_length=255
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=100
    )
    address = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        ordering = ('phone',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.phone}, {self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
