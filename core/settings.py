import os
from . import jazzmin
from . import restaurant_apps
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# ----------- Debugging Mode -----------
# WHEN CHANGING RUN python manage.py collectstatic
DEBUG = True
#
# if not DEBUG:
#     SECURE_HSTS_SECONDS = 60
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
# ----------------------------------------------------------------


# ------------ Hosting Settings --------------------
ALLOWED_HOSTS = ['127.0.0.1', 'sgiorkas.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://sgiorkas.pythonanywhere.com']
# ----------------------------------------------------------------


# ----------- Application definition --------------
INSTALLED_APPS = [
    'main.apps.MainConfig',
    'menu.apps.MenuConfig',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'guest_user',
]
INSTALLED_APPS += restaurant_apps.NEW_APPS
# ----------------------------------------------------------------


# --------- Custom Admin Definition ---------
JAZZMIN_SETTINGS = jazzmin.JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = jazzmin.JAZZMIN_UI_TWEAKS
# ----------------------------------------------------------------


# --------- Middleware ----------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]
# ----------------------------------------------------------------

ROOT_URLCONF = 'core.urls'

# ---------- Templates ----------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
# ----------------------------------------------------------------


# ---------- Static files (CSS, JavaScript, Images) ----------
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# ----------------------------------------------------------------

WSGI_APPLICATION = 'core.wsgi.application'

# ---------- Database ----------
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# ----------------------------------------------------------------


# ----------- Password validation -----------
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # guest should be the last entry to prevent unauthorized access
    "guest_user.backends.GuestBackend",
]
# ----------------------------------------------------------------


# ---------- Internationalization ----------
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en'
LANGUAGES = [("en", "English"), ("el", "Greek")]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# ----------------------------------------------------------------


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# ----------- Session & Guest Options -----------
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 43200  # 12 hours

# Guest Options
GUEST_USER_NAME_GENERATOR = 'guest_user.functions.generate_numbered_username'
GUEST_USER_MAX_AGE = 43200  # 12 HOURS
# ----------------------------------------------------------------
