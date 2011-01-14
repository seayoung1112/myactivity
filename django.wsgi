import os
import sys
import django.core.handlers.wsgi

path = '/home/zsc/myactivity'
if path not in sys.path:
    sys.path.append(path)

path = '/home/zsc'
if path not in sys.path:
    sys.path.append(path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'myactivity.settings'
application = django.core.handlers.wsgi.WSGIHandler()
