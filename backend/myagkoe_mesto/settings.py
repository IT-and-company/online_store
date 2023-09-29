import os
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR.parent, '.env'))

SECRET_KEY = env(
    'SECRET_KEY',
    default='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'
)

DEBUG = int(env("DEBUG", default=0))

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'phonenumbers',
    'psycopg2',
    'djoser',
    'smart_selects',
    'corsheaders',

    'api',
    'client',
    'products',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'myagkoe_mesto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myagkoe_mesto.wsgi.application'

if env("USE_SQLITE", default="True") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": env("BASE_DIR", default='db.sqlite3')
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env(
                "DB_ENGINE", default="django.db.backends.postgresql"),
            "NAME": env("DB_NAME", default="postgres"),
            "USER": env("POSTGRES_USER", default="postgres"),
            "PASSWORD": env("POSTGRES_PASSWORD", default="postgres"),
            "HOST": env("DB_HOST", default="db"),
            "PORT": env("DB_PORT", default="5432"),
        },
    }

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.NumericPasswordValidator'),
    },
]

# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'backend_static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'backend_media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': ('rest_framework.pagination.'
                                 'PageNumberPagination'),

    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S %Z",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str(env('EMAIL_HOST'))  # Адрес SMTP-сервера
EMAIL_PORT = str(env('EMAIL_PORT'))  # Порт SMTP-сервера (обычно 587 для TLS)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = None  # Тайм-аут соединения
EMAIL_HOST_USER = str(env('EMAIL_HOST_USER'))  # Ваш адрес электронной почты
EMAIL_HOST_PASSWORD = str(env('EMAIL_HOST_PASSWORD'))  # Ваш пароль от почты
DEFAULT_FROM_EMAIL = str(
    env('EMAIL_HOST_USER'))  # Адрес отправителя по умолчанию
DEFAULT_TO_EMAIL = str(
    env('DEFAULT_TO_EMAIL'))  # Адрес получателя по умолчанию

MAX_LENGTH_1 = 250
MAX_LENGTH_2 = 7
MAX_LENGTH_3 = 15
MIN_VALUE = 1

CSRF_TRUSTED_ORIGINS = [
    "http://*localhost",
    "https://*localhost",
    "http://*127.0.0.1",
    "https://*127.0.0.1",
    "http://*mebelnyibutikmm.ru",
    "https://*mebelnyibutikmm.ru",
    "http://*mebelnyibutikmm.store",
    "https://*mebelnyibutikmm.store",
    "http://*xn--90aakbqejefiag1en1joa.xn--p1ai",
    "https://*xn--90aakbqejefiag1en1joa.xn--p1ai",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CART_SESSION_ID = 'cart'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'api.auth_backend.AuthenticationWithoutPassword',
)

CORS_ORIGIN_ALLOW_ALL = True
