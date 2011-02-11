from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from models import ActivityType
from views import *

urlpatterns = patterns('',
    (r'^create/$', create),
    (r'^createtype/$', create_type),
    (r'^detail/(?P<activity_id>\d+)/$', detail),
    (r'^edit/(?P<activity_id>\d+)/$', edit),
    (r'^invite/(?P<activity_id>\d+)/$', invite),
    (r'^apply/(?P<activity_id>\d+)/$', apply),
    (r'^join/(?P<activity_id>\d+)/$', join),
    (r'^quit/(?P<activity_id>\d+)/$', quit),
    (r'^wait/(?P<activity_id>\d+)/$', wait),
    (r'^check/(?P<activity_id>\d+)/$', check),
    (r'^setdefault/$', set_type_default),
    (r'^home/$', home),
    (r'^ajax/type/(?P<type_id>\d+)/$', get_type_default),
    (r'^friend-candidates/(?P<activity_id>\d+)/$', get_friend_candidates),
    (r'^potential-candidates/(?P<activity_id>\d+)/$', get_potential_candidates),
)
