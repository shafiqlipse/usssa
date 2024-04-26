from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m3ex5s$yd@*j#(gw0!wisdlc$y7)hpzem8c0l90)+g(y+a6uar"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "django_select2",
    "accounts",
    "school",
    "dashboard",
    "athletes",
    # "ckeditor",
    # "ckeditor_uploader",
    "football",
    # "basketball3",
    # "basketball5",
    "client",
    "officials",
    "transfers",
    # "dynamic_breadcrumbs",
    # "news",
    # "utils",
    "champs",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "accounts.middleware.CurrentPageMiddleware"
]

ROOT_URLCONF = "usssa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dynamic_breadcrumbs.context_processors.breadcrumbs",
                # "transfers.context_processors.view_notifications"
                # "utils.context_processors.champrionship",
            ],
        },
    },
]

WSGI_APPLICATION = "usssa.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "sec",
        "USER": "root",
        "PASSWORD": "Remmystar@48.com",
        "HOST": "localhost",  # or the hostname where your MySQL server is running
        "PORT": "3306",  # or the port on which your MySQL server is listening
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Kampala"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


import os

STATIC_URL = "static/"
MEDIA_URL = "uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "accounts", "static"),
    # os.path.join(BASE_DIR, "client", "static"),
    # os.path.join(BASE_DIR, "athletes", "static"),
    # os.path.join(BASE_DIR, "officials", "static"),
]
CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
USE_DJANGO_JQUERY = True
# CKEDITOR_JQUERY_URL = 'path/to/your/jquery.min.js'
# CKEDITOR_BASEPATH = 'path/to/your/ckeditor/ckeditor/'

# IMPORT_EXPORT_USE_TRANSACTIONS = True
# ALLOWED_HOSTS = ["localhost", "127.0.0.1", "beb9-41-210-147-42.ngrok-free.app", "*"]
# settings.py

# # Use secure cookies for session and authentication
SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # Redirect all HTTP requests to HTTPS
# SECURE_SSL_REDIRECT = True

# # settings.py

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# # # Set HSTS header to force HTTPS for a specified duration (optional)
# # SECURE_HSTS_SECONDS = 31536000  # 1 year
# # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# # SECURE_HSTS_PRELOAD = True

# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # Example email settings (replace with your actual settings)

# settings.py==========smtp
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ssekittoshafiq@gmail.com"  # Your Gmail address
EMAIL_HOST_PASSWORD = "gyow rrgb nxvu mktx"  # Use the generated app password

# ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
