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

# from sms_config import SMSTransport


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)
                + six.text_type(user.is_active))


def create_confirmation_code() -> int:
    return random.randint(1000, 9999)


# def send_confirmation_code(user):
#     api_id = settings.env('API_ID_SMS')
#     sms = SMSTransport(api_id)
#     result = sms.send(
#         user.phone,
#         f'Ваш код для подтверждения: {user.confirmation_code}')
#     print(result)


def send_confirmation_link(request: HttpRequest, user_data: dict) -> None:
    current_site = get_current_site(request)
    user = User.objects.get(email=user_data['email'])
    account_activation_token = TokenGenerator()
    token = account_activation_token.make_token(user)
    title_mail = ('Ссылка для подтверждения аккаунта была отправлена на '
                  'указанный адрес')
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
