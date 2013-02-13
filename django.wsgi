import os
import sys

os.environ['DJANGO_SETTINGS_MOUDLE'] = 'website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()