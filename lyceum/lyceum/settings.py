import os
import pathlib

import dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

dotenv.load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fake_key")

debug_str_value = str(os.getenv("DJANGO_DEBUG"))
DEBUG = debug_str_value.lower() in (
    "true",
    "yes",
    "1",
    "y",
    "t",
)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage.apps.HomepageConfig",
    "catalog.apps.CatalogConfig",
    "about.apps.AboutConfig",
    "core.apps.CoreConfig",
    "sorl.thumbnail",
    "django_dump_load_utf8",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG is True:
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    INSTALLED_APPS += ("debug_toolbar",)
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

ALLOW_REVERSE = str(
    os.getenv("DJANGO_ALLOW_REVERSE", default=True),
).lower() in (
    "true",
    "yes",
    "1",
    "y",
)

if ALLOW_REVERSE:
    MIDDLEWARE += ("lyceum.middleware.ReverseWordsMiddleware",)

ROOT_URLCONF = "lyceum.urls"

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
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_CHARSET = "utf-8"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
