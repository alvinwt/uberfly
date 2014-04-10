# Django settings for mysite project.
import os, os.path, django
from os.path import abspath, dirname
DEBUG = True
TEMPLATE_DEBUG = False

ADMINS = (
     ('Alvin', 'a0073895@nus.edu.sg'),
)

MANAGERS = ADMINS

SEND_BROKEN_LINK_EMAILS = True

ENCRYPTED_FIELD_KEYS_DIR = ()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mysql',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'gtklab',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

INTERNAL_IPS = ('172.31.19.193')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.uberfly.org', '.uberfly.org.']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Singapore'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

LANGUAGES = [
    ('en','English'),]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = abspath(os.path.join(dirname(__file__),os.pardir))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = '/home/lichenhao/djangosite/loq/media/'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/ubuntu/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = ('/home/ubuntu/project/loq/static/',)
#                    '/home/lichenhao/Dropbox/djangosite/loq/static/loq/'

STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__),'static'),
                    os.path.join(SITE_ROOT, 'static'),
)
# Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',

)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h3j)=l1v9e_l%yc8s&e9de09-6f7+_y+6@0dk&yy^mr@*2*dyi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.static',
                               'django.core.context_processors.csrf',
                               'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
     'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
     'django.contrib.messages.middleware.MessageMiddleware',
     'debug_toolbar.middleware.DebugToolbarMiddleware',
     'django.middleware.doc.XViewMiddleware',
     'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'loq.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'loq.wsgi.application'

TEMPLATE_DIRS = (
#"/home/lichenhao/Dropbox/djangosite/loq/Templates/loq",
#"/home/lichenhao/Dropbox/djangosite/loq/Templates",
#os.path.join(os.path.dirname(__file__),'Templates'),
os.path.join(SITE_ROOT, 'Templates'),
os.path.join(SITE_ROOT, 'Templates/loq'),
# Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'django.contrib.admin',
     'django.contrib.admindocs',
     'django.contrib.comments',
     'favit',
     'django.contrib.sites',
     'django.contrib.flatpages',
     'debug_toolbar',
     'django_extensions',
     'south',
     'django_tables2',
     'rest_framework',
     'django_filters',
     'dbbackup',
     'csvimport',
     'django_pandas',
     'loq',
    'gunicorn'
)
LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/interval/'
SESSION_ENGINE = "django.contrib.sessions.backends.cache" 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

SOUTH_TESTS_MIGRATE=False
SKIP_SOUTH_TESTS= True

DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_FILESYSTEM_DIRECTORY = '/mnt/fly-data/backups'
#DBBACKUP_TOKENS_FILEPATH = '/home/lichenhao/Dropbox/tokens/tokens'
#DBBACKUP_DROPBOX_APP_KEY = '1h717o0tvdtn3nd'
#DBBACKUP_DROPBOX_APP_SECRET = 'pkuw8m9ymgf1473'

DEBUG_TOOLBAR_PANELS = (
           'debug_toolbar.panels.version.VersionDebugPanel',
           'debug_toolbar.panels.timer.TimerDebugPanel',
           'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
           'debug_toolbar.panels.headers.HeaderDebugPanel',
           'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
           'debug_toolbar.panels.template.TemplateDebugPanel',
           'debug_toolbar.panels.sql.SQLDebugPanel',
           'debug_toolbar.panels.signals.SignalDebugPanel',
           'debug_toolbar.panels.logger.LoggingPanel',
       
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
