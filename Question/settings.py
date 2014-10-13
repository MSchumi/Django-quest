#coding:utf-8
"""
Django settings for Question project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)).replace("\\","/")
import logging
logging.basicConfig(
level = logging.DEBUG,
format = '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d%(message)s',
filename = 'filelog.log',  
)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l##gz+i+gqho%iej(m9cv2xdk%w#1trgk3nw90i-#f=0=@0+p%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'quest',
    'account',
    'feed',
    'debug_toolbar',
    'djcelery',
    #'haystack',
    #'solr',
    'testpp',
    #'avatar',
    'notification',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'notification.message.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
  
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    'notification.processor.message_processor',
)

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]



ROOT_URLCONF = 'Question.urls'
WSGI_APPLICATION = 'Question.wsgi.application'
LOGIN_URL='/account/' #login_require 配置参数#

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'quest',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

# extend user 
AUTH_USER_MODEL = 'account.User'
AUTHENTICATION_BACKENDS=('account.auth.UserAuth',)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'#windows下貌似无效#
USE_TZ=True
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

debug_toolbar='E:/python/Lib/site-packages/django_debug_toolbar-1.2.1-py2.7.egg/debug_toolbar/templates'

TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'template'),
        os.path.join(BASE_DIR,'quest/template'),
        os.path.join(BASE_DIR,'account/template'),
        os.path.join(BASE_DIR,'notification/template'),
        debug_toolbar,
        )

QUESTION_RUL="127.0.0.1:8000"

EMAIL_HOST='smtp.163.com'
EMAIL_PORT='25'
EMAIL_HOST_USER='msliudongsheng@163.com'
EMAIL_HOST_PASSWORD='MSLDS6560631'
EMAIL_SUBJECT_PREFIC='F1论坛'
EMAIL_USE_TLS=True
SERVER_EMAIL='msliudongsheng@163.com'

#celery参数配置
import djcelery
djcelery.setup_loader()
#from kombu import serialization
#serialization.registry._decoders.pop("application/x-python-serialize")
CELERY_ACCEPT_CONTENT=['json','pickle']
CELERY_TASK_SERIALIZER ='json'
CELERY_RESULT_SERIALIZER ='json'
BROKER_URL="amqp://guest:guest@localhost:5672/"

#solr 服务地址和核心配置
SOLR_URL="http://127.0.0.1:8080/solr/"
QUESTION_CORE='question'
USER_CORE='user'
ANSWER_CORE='answer'

#redis 连接
REDIS_IP="127.0.0.1"
REDIS_PORT="6379"


