import os
from urllib.parse import quote

import environ


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

# Load env to get settings
env = environ.Env()

SECRET_KEY = env.str("SECRET_KEY", default="dummy-key")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]
if not DEBUG:
    ALLOWED_HOSTS = [env.str("HOST", default="google.com")]

USE_TZ = True
TIME_ZONE = "Europe/Tallinn"

CSRF_USE_SESSIONS = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "main",
    "accounts",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    # When using DATABASE_URL, unsafe characters in the url should be encoded.
    # See: https://django-environ.readthedocs.io/en/latest/#using-unsafe-characters-in-urls
    "default": env.db_url(
        "DATABASE_URL",
        default="psql://{user}:{password}@{host}:{port}/{name}?sslmode={sslmode}".format(
            host=env.str("DATABASE_HOST", default="postgres"),
            port=env.int("DATABASE_PORT", default=5432),
            name=quote(env.str("DATABASE_NAME", default="nofrontend")),
            user=quote(env.str("DATABASE_USER", default="nofrontend")),
            password=quote(env.str("DATABASE_PASSWORD", default="nofrontend")),
            sslmode=env.str("DATABASE_SSLMODE", default="disable"),
        ),
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]
AUTH_USER_MODEL = "accounts.CustomUser"


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join("/app", "static"),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_FROM_EMAIL = "No Frontend Admins <admins@nofrontend.com>"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 1025
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "en-us"
LANGUAGES = WAGTAIL_CONTENT_LANGUAGES = [
    ("en-us", "English"),
]
