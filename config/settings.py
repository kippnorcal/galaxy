import os
import rollbar

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD="django.db.models.AutoField"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "catalog.apps.CatalogConfig",
    "accounts.apps.AccountsConfig",
    "high_health.apps.HighHealthConfig",
    "analytics.apps.AnalyticsConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
        "django.utils.autoreload": {"level": "INFO"},
        "django.db.backends": {"level": "INFO"},
        "console": {
            "handlers": ['console'],
            "level": "INFO",
            "propagate": True
        },
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(os.path.join(BASE_DIR, "templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "catalog.views.navbar",
            ],
            "libraries": {
                "feedback_helpers": "templatetags.feedback_helpers",
                "high_health_helpers": "templatetags.high_health_helpers",
                "nav_helpers": "templatetags.nav_helpers",
            },
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://stg.kippgalaxy.org",
    "https://kippgalaxy.org"
    ]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 250,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/staticfiles/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
SAML_FOLDER = os.path.join(BASE_DIR, "saml")

SESSION_ENGINE = "django.contrib.sessions.backends.file"
TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"
LOGIN_URL = "/login/"
if int(os.getenv("SSL", default=0)):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

USE_X_FORWARDED_PORT = True

ROLLBAR = {
    "access_token": os.getenv("ROLLBAR_TOKEN"),
    "environment": "development" if DEBUG else "production",
    "root": BASE_DIR,
}
rollbar.init(**ROLLBAR)
