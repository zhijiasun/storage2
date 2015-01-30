"""
Django settings for side project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l$tf6j3%xtlmfo(2kl^wp59-hq%v+d+nvxsm@^l1f5ico@(4%6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'xadmin',
    'crispy_forms',
    #'reversion',
    'rest_framework',
    'rest_framework.authtoken',
    'epm',
    'ams',  #app management system
    'xcms',
    'import_export',
    'gunicorn',
    'registration',
    'rest_auth',
    'south',
)

MIDDLEWARE_CLASSES = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'side.urls'

WSGI_APPLICATION = 'side.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'epm',
	'USER': 'postgres',
	'PASSWORD': '12345678',
	'PORT':'',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'
# MEDIA_ROOT = '/home/jasonsun/svn_repo/'
MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_RENDERER_CLASSES':('rest_framework.renderers.JSONRenderer',),
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework.authentication.BasicAuthentication',),
    'PAGINATE_BY': 10
}

# REST_REGISTRATION_BACKEND = 'registration.backends.simple.views.RegistrationView'#we can define our own View
#REST_PROFILE_MODULE = 'auth.User'#here we can define our own UserProfile
REST_REGISTRATION_BACKEND = 'epm.views.RegistrationView'#we can define our own View
REST_PROFILE_MODULE = 'epm.UserProfile'#here we can define our own UserProfile

AUTH_PROFILE_MODULE='epm.UserProfile'

LOGGING = {
        'version':1,
}
# INTERNAL_IPS=('135.242.96.163',)
# def show_toolbar(request):
#     return True
# SHOW_TOOLBAR_CALLBACK = show_toolbar

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

LOGIN_REDIRECT_URL = '/xadmin/'

#log configuration
LOG_FILE = '/tmp/epm.log'
LOG_DJANGO = '/tmp/django.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(module)s : %(message)s'
        },
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILE,
            'mode': 'a',
        },
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_DJANGO,
            'mode': 'a',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        # '': {
        #     'handlers': ['file', 'console'],
        #     'level': 'INFO',
        #     'propagate': True,
        # },
        'django': {
            'handlers': ['django_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'epm': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'rest_auth': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        # 'django.request': {
        #     'handlers': ['mail_admins', 'console'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
    }
}
EMAIL_HOST='smtp.163.com'
EMAIL_PORT=25
EMAIL_HOST_USER='szjrabbit@163.com'
EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='szjrabbit@163.com'
