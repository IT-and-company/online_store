import random

import six
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from typing import Any

from client.cart import Cart
from client.models import Order


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    """Класс, отвечающий за генерацию токена."""
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)
                + six.text_type(user.is_active))


def create_confirmation_code() -> int:
    """Функция, возвращающая случайное число от 1000 до 9999."""
    return random.randint(1000, 9999)


def send_confirmation_link(request: HttpRequest, user_data: dict) -> None:
    """Функция, которая отправляет пользователю ссылку-подтверждение
    для завершения активации."""
    current_site = get_current_site(request)
    user = User.objects.get(email=user_data['email'])
    account_activation_token = TokenGenerator()
    token = account_activation_token.make_token(user)
    title_mail = 'Ссылка для подтверждения аккаунта'
    message = render_to_string('activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    plain_message = strip_tags(message)
    send_mail(
        title_mail,
        plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email,),
        html_message=message
    )


def send_confirmation_link_for_login(
        request: HttpRequest, user_data: dict) -> None:
    """Функция, которая отправляет пользователю ссылку-подтверждение для
    входа на сайт."""
    current_site = get_current_site(request)
    user = User.objects.get(email=user_data['email'], is_active=True)
    account_activation_token = TokenGenerator()
    token = account_activation_token.make_token(user)
    title_mail = 'Ссылка для подтверждения входа на сайт'
    message = render_to_string('login.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    plain_message = strip_tags(message)
    send_mail(
        title_mail,
        plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email,),
        html_message=message
    )


def get_cart(request):
    return (Cart(request=request, from_db=True)
            if request.user.is_authenticated
            else Cart(request=request))


def send_order(
        subject: str,
        template: str,
        to_email: tuple[Any],
        order: Order,
        cart: Cart,
        cart_items: list[dict[str, Any]]
) -> None:
    html_message = render_to_string(
        template,
        {
            'order': order,
            'cart_items': cart_items,
            'total_price': cart.get_total_price(),
            'total_quantity': len(cart),
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=to_email,
        html_message=html_message)
