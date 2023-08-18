import random


def create_confirmation_code() -> int:
    return random.randint(1000, 9999)


def send_confirmation_code(phone):
    pass
