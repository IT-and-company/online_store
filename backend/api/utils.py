import random

from django.conf import settings

from sms_config import SMSTransport


def create_confirmation_code() -> int:
    return random.randint(1000, 9999)


def send_confirmation_code(user):
    api_id = settings.env('API_ID_SMS')
    sms = SMSTransport(api_id)
    result = sms.send(
        user.phone,
        f'Ваш код для подтверждения: {user.confirmation_code}')
    print(result)
