from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    phone = PhoneNumberField(
        'phone',
        null=False,
        blank=False,
        unique=True,
        help_text='Введите ваш телефон'
    )
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    address = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=True)
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
    def is_active(self):
        return self.active
    
    @property
    def is_staff(self):
        return self.is_admin