from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from models import ActivityType
from views import *

urlpatterns = patterns('',
    (r'^create/$', create),
    (r'^createtype/$', create_type),
    (r'^detail/(?P<activity_id>\d+)/$', detail),
    (r'^edit/(?P<activity_id>\d+)/$', edit),
    (r'^reply/(?P<activity_id>\d+)/$', reply),
    (r'^invite/(?P<activity_id>\d+)/$', invite),
    (r'^setdefault/$', set_type_default),
    (r'^home/$', home),
    (r'^ajax/type/(?P<type_id>\d+)/$', get_type_default),
)
