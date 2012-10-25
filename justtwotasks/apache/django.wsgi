import os
import sys

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(app_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'justtwotasks.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
