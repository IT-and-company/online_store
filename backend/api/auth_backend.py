from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class AuthenticationWithoutPassword(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        if email is None:
            email = request.data.get('email', '')
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
