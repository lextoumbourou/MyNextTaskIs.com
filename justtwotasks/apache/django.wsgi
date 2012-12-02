import os
import sys
import site
import private

app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(app_path)

# Remember original sys.path.
prev_sys_path = list(sys.path)

site.addsitedir(private.SITE_DIR)

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'justtwotasks.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
