# Django settings for website project.
import os
import sys
from website.utils import build_info

rootPath = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'apwan.UserProfile'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc "{infile}" "{outfile}"'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(rootPath + '/static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = 'dmwawhazvr_7b01q7v92k&amp;bo9w%+$wqqgyszk##a_5^reykd2_'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',

    'website.utils.context_processors.template_settings'
)

# Settings to add to template contexts
# (website.utils.context_processors.template_settings)
TEMPLATE_SETTINGS = [
    # Fruct.us settings
    'FRUCTUS_DEPLOYMENT',

    # Build Info
    'BUILD_INFO_EXISTS',
    'BUILD_INFO_HTML',
    'BUILD_ID',
    'BUILD_NUMBER',
    'GIT_BRANCH',
    'GIT_COMMIT',
    'UPSTREAM_BUILD_NUMBER',
    'UPSTREAM_JOB_NAME'
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'


BASE_URL = None  # Automatically determine our URL


def build_url(request, path):
    global BASE_URL
    if not BASE_URL:
        BASE_URL = "http://" + request.META['HTTP_HOST']
    return BASE_URL + path


LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/home'

WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
    os.path.abspath(rootPath + '/website/templates/')
)

JSTEMPLATE_DIRS = [
    os.path.abspath(rootPath + '/website/jstemplates/')
]

CRISPY_TEMPLATE_PACK = 'bootstrap'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pyflakes',
    'website.jenkins_tasks.run_pep8',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

PROJECT_APPS = [
    'website.apwan',
    'website.utils',
]

# Add 'secrets' (Website Secrets) project if it exists
if os.path.exists(os.path.abspath(rootPath + '/secrets/')):
    PROJECT_APPS.append('secrets')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'django_jenkins',

    'dajax',
    'dajaxice',
    'crispy_forms',
    'sekizai',
    'jstemplate',
    'json_field',
    'compressor',

    'django_like',
    'south',
] + PROJECT_APPS

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

#
# Fruct.us Settings
#

# Current deployment environment
#   INTERNAL - Internal Deployment (API requires auth with staff accounts)
#   INVITE   - Invite / Private Deployment (API requires auth with any account)
#   OPEN     - Open Deployment (API requires no auth + registration is open)
FRUCTUS_DEPLOYMENT = 'INTERNAL'

FRUCTUS_KEYS = None
# try import 'secrets.keys'
try:
    import secrets.keys as FRUCTUS_KEYS
except ImportError:
    # try fallback to importing 'website.keys'
    try:
        import website.keys as FRUCTUS_KEYS
    except ImportError:
        print "ERROR: No keys available!"


def load_deployment_settings():
    for key, value in FRUCTUS_DEPLOYMENT_SETTINGS.__dict__.items():
        if not key.startswith('__') and not key.endswith('__'):
            setattr(sys.modules[__name__], key, value)

# Import deployment settings
try:
    import secrets.settings_deploy as FRUCTUS_DEPLOYMENT_SETTINGS
    load_deployment_settings()
except ImportError:
    try:
        import settings_deploy as FRUCTUS_DEPLOYMENT_SETTINGS
        load_deployment_settings()
    except ImportError:
        pass

#
# Load build information (build.json)
#

BUILD_INFO = build_info.load(rootPath + "/build.json")
BUILD_INFO_EXISTS = len(BUILD_INFO) != 0
BUILD_INFO_HTML = build_info.to_html(BUILD_INFO)

BUILD_ID = BUILD_INFO.get('BUILD_ID')
BUILD_NUMBER = BUILD_INFO.get('BUILD_NUMBER')
GIT_BRANCH = BUILD_INFO.get('GIT_BRANCH')
GIT_COMMIT = BUILD_INFO.get('GIT_COMMIT')
GIT_COMMIT_SHORT = BUILD_INFO.get('GIT_COMMIT_SHORT')
UPSTREAM_BUILD_NUMBER = BUILD_INFO.get('UPSTREAM_BUILD_NUMBER')
UPSTREAM_JOB_NAME = BUILD_INFO.get('UPSTREAM_JOB_NAME')

if BUILD_INFO_EXISTS and DEBUG:
    print "------------------------- BUILD INFO -------------------------"
    print "BUILD_INFO_EXISTS\t", BUILD_INFO_EXISTS
    print "BUILD_ID\t\t", BUILD_ID
    print "BUILD_NUMBER\t\t", BUILD_NUMBER
    print "GIT_BRANCH\t\t", GIT_BRANCH
    print "GIT_COMMIT\t\t", GIT_COMMIT
    print "UPSTREAM_BUILD_NUMBER\t", UPSTREAM_BUILD_NUMBER
    print "UPSTREAM_JOB_NAME\t", UPSTREAM_JOB_NAME
    print "--------------------------------------------------------------"
