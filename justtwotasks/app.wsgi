import os
import sys

import private

sys.path.append(private.APP_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'justtwotasks.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
