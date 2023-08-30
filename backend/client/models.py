from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from products.models import VariationProduct, User


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


class UserCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )

    def __str__(self):
        return f'Корзина {self.user.get_username()}'


class OrderCart(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='cart'
    )

    def __str__(self):
        return f'Корзина {self.order}'


class CartProductBase(models.Model):
    quantity = models.IntegerField(
        default=0,
        verbose_name='Количество'
    )

    product = models.ForeignKey(
        VariationProduct,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )

    class Meta:
        abstract = True


class CartProduct(CartProductBase):

    cart = models.ForeignKey(
        UserCart,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='products'
    )

    def __str__(self):
        return f'{self.product} в корзине {self.cart}'


class OrderProduct(CartProductBase):

    cart = models.ForeignKey(
        OrderCart,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='products'
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Цена'
    )

    def __str__(self):
        return f'{self.product} в заказе {self.cart}'
