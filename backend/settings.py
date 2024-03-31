from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config

# Carregar variáveis de ambiente do arquivo .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv()
# Configurações básicas
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='mysecretkey')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    'nutricliniapi-production.up.railway.app',
    'https://nutricliniapi-production.up.railway.app',
    'localhost', 
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'http://nutricliniapi-production.up.railway.app',
    'https://nutricliniapi-production.up.railway.app',
    'localhost:8000', 
    'localhost:3000', 
    'localhost:3030', 
    '127.0.0.1:8000', 
    '127.0.0.1:3000', 
    '127.0.0.1:3030', 
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.core.mail',
    #apps
    'apps.tokenProfile',
    'apps.appointments',
    'apps.locations',
    'apps.messageClini',
    'apps.consultation',
    'apps.nutritionist',
    'apps.patient',
    #libs
    'corsheaders',
    "rest_framework",
    'rest_framework.authtoken',
    'djoser',
    "drf_spectacular",
    'django_filters'
]

if config("USE_POSTGRES", False):
    INSTALLED_APPS += [
        'django.contrib.postgres',
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }
    }
]

WSGI_APPLICATION = "backend.wsgi.application"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=1),
}

if config('USE_POSTGRES', default=False, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('PGHOST'),
            'PORT': config('PGPORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configurações de idioma e fuso horário
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Diretório onde os arquivos estáticos serão coletados

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurações de envio de email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'Nutriclinicn <nutriclinicn@gmail.com>'
