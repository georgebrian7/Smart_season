"""
Django settings for smartseason project.

Environment-backed configuration: loads .env in development and reads common variables from the environment.
"""

from pathlib import Path
import os
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file at the project root when present
load_dotenv(BASE_DIR / '.env')

# SECURITY: Read secret and debug from environment
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'change-me-in-production')

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

# Hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if os.getenv('DJANGO_ALLOWED_HOSTS') else []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'application',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartseason.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smartseason.wsgi.application'


# Database configuration
# Use DATABASE_URL if provided (postgres, mysql, sqlite), otherwise default to bundled sqlite3
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Simple parsing of DATABASE_URL into Django DATABASES dictionary
    parsed = urlparse(DATABASE_URL)
    scheme = parsed.scheme

    if scheme.startswith('postgres') or scheme == 'postgresql':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed.path.lstrip('/'),
                'USER': unquote(parsed.username) if parsed.username else '',
                'PASSWORD': unquote(parsed.password) if parsed.password else '',
                'HOST': parsed.hostname or '',
                'PORT': parsed.port or '',
            }
        }
    elif scheme == 'sqlite' or DATABASE_URL.endswith('.sqlite3'):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, parsed.path.lstrip('/')),
            }
        }
    else:
        # Fallback: attempt sqlite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'application.CustomUser'

# Authentication/redirect settings
LOGIN_URL = 'auth:login'
LOGIN_REDIRECT_URL = 'auth:admin_dashboard'
LOGOUT_REDIRECT_URL = 'auth:login'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Notes: expected environment variables (create a .env at project root or set in your environment):
# - DJANGO_SECRET_KEY
# - DJANGO_DEBUG (True/False)
# - DATABASE_URL (optional, e.g. postgres://user:pass@host:5432/dbname)
# - DJANGO_ALLOWED_HOSTS (comma-separated)
