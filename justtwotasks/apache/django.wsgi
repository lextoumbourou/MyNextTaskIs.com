import os
import sys

sys.path.append('/srv/justtwotasks.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'justtwotasks.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
