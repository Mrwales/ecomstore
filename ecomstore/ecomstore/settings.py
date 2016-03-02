"""
Django settings for ecomstore project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT, \
    LOGIN_REDIRECT_URL, STATIC_ROOT
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gg&4l(cl5$(nsqsbv=7d2qz0+hao&^4s7lm4qq$ubds_g3x&!3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Change to true before deploying into production
ENABLE_SSL = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'catalog',
    'utils',
    'cart',
    'checkout',
    'account',
    'search',
    'stats',
    'tagging',
    'marketing',
   # 'paypal.standard.ipn',
    # 'djstripe',
    # 'djangodblog',
]

AUTHNET_POST_URL = 'test.authorize.net'
AUTHNET_POST_PATH = '/gateway/transact.dll'
AUTHNET_LOGIN = '44WjKEC3dd'
AUTHNET_KEY = '9B6U5V3uJuSa3H2c'

CANON_URL_HOST = 'www.fly-shoes.com'  # site to which we will redirect our users
CANON_URLS_TO_REWRITE = ['fly-shoes.com', 'modernshoes.com']  # list of hostnames that, if detected, will be redirected to our canonical hostname
# PAYPAL_RECEIVER_EMAIL = "wale_adesina11@yahoo.com"

# STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_live_CljyAKLjqlsxoYvGmOfCYOtR")
# STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_7NOIioSCbOYcP0paSMyFjvLB")
# DJSTRIPE_PLANS = {
#     "monthly": {
#         "stripe_plan_id": "pro-monthly",
#         "name": "Web App Pro ($25/month)",
#         "description": "The monthly subscription plan to WebApp",
#         "price": 2500,  # $25.00
#         "currency": "usd",
#         "interval": "month"
#     },
#     "yearly": {
#         "stripe_plan_id": "pro-yearly",
#         "name": "Web App Pro ($199/year)",
#         "description": "The annual subscription plan to WebApp",
#         "price": 19900,  # $199.00
#         "currency": "usd",
#         "interval": "year"
#     }
# }

AUTH_PROFILE_MODULE = 'accounts.userprofile'

SITE_NAME = 'Fly Shoes'
META_KEYWORDS = 'Shoes, footwears, buy shoes, shoe supplies'
META_DESCRIPTION = 'Fly Shoes is an online supplier of shoes for stylist,fashionist,young and old'

PRODUCTS_PER_PAGE = 12
PRODUCTS_PER_ROW = 4

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'SSLMiddleware.SSLRedirect',
    'marketing.urlcanon.URLCanonicalizationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
]

ROOT_URLCONF = 'ecomstore.urls'

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
                'utils.context_proc.ecomstore',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
             'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': 'db.sqlite3',
                        }
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2' ,
#         'USER': 'root',
#         'NAME':'walemusicstore',
#         'PASSWORD': 'celebrate',
#         'HOST':'127.0.0.1',
#         'PORT':'5432',
#     }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'store_static')
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static'),
    
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'store_media')
LOGIN_REDIRECT_URL = '/account/my_account/'
