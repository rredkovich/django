"""
Django settings for restaurant project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASES = {'default' :dj_database_url.config()}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

#GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
#GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

#GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(environ.get('GEOS_LIBRARY_PATH'))
#GDAL_LIBRARY_PATH = "{}/libgdal.so".format(environ.get('GDAL_LIBRARY_PATH'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

#TODO Change in production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6+)idbqp^jvtw3q!*((=b)u9ba70)2p19#yoa4bc6zrvowl12r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'api',
    'south',
    'social.apps.django_app.default',
    'bootstrap3',
    # pinax-account apps:
    "ppacc",
    "bootstrapform",
    "pinax_theme_bootstrap",
    "account",
    "eventlog",
    "metron",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'restaurant.urls'

WSGI_APPLICATION = 'restaurant.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#TODO Change in production
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'restaurant2',
        'USER': 'muhammadali',
        'PASSWORD': "postgres",
        'HOST': 'localhost',
        'PORT': 5432
    }
}

POSTGIS_VERSION = (2, 1, 2)

# Python-social-auth section
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.facebook.FacebookOAuth2',
    'account.auth_backends.UsernameAuthenticationBackend',

)

#TODO Change in production
SOCIAL_AUTH_FACEBOOK_KEY = '338877252958705'
SOCIAL_AUTH_FACEBOOK_SECRET = '104976a391991584da7dbd3fa192315f'


TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "account.context_processors.account",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "pinax_theme_bootstrap.context_processors.theme",
)

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name']

LOGIN_URL = '/login/facebook/'
# LOGIN_REDIRECT_URL = '/restaurants/01/comment'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# SESSION_COOKIE_DOMAIN = "128.199.176.172"

#TODO Change to actual smtp account for production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'redkovich@gmail.com'
EMAIL_HOST_PASSWORD = 'vkiofcumunkmixrj'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_PATH = os.path.join(BASE_DIR,'static')


STATIC_ROOT = '/home/django/django_project/static'
#STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)
#STATICFILES_DIRS = ( os.path.join('static'),)
#MEDIA_ROOT = '/home/django/django_project/static'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "/api/templates"),
)
