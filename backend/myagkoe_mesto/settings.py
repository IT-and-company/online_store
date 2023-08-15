import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR.parent, '.env'))

SECRET_KEY = env('SECRET_KEY', default='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs')

DEBUG = int(env("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'phonenumbers',
    'psycopg2',
    'djoser',

    'api',
    'products',
    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
            "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
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
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
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
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

MAX_LENGTH_1 = 200
MAX_LENGTH_2 = 7
MAX_LENGTH_3 = 20
MIN_VALUE = 1

CSRF_TRUSTED_ORIGINS = [
    "https://*localhost:1337",
    "http://*localhost:1337",
    "https://*127.0.0.1:1337",
    "http://*127.0.0.1:1337",
    f"http://*{env('DOMAIN_URL')}",
    f"https://*{env('DOMAIN_URL')}",
    ]