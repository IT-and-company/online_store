from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('Пользователям необходим Email адрес')
        if not phone:
            raise ValueError('Пользователям необходим номер телефона')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None):
        user = self.create_user(
            email=email,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
