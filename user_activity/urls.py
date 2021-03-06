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
    (r'^poll/(?P<activity_id>\d+)/$', poll),
    (r'^check/(?P<activity_id>\d+)/$', check),
    (r'^post/(?P<activity_id>\d+)/$', post),
    (r'^persons/(?P<activity_id>\d+)/(?P<type>\w+)/$', get_persons),
    (r'^setdefault/$', set_type_default),
    (r'^home/$', home),
    (r'^ajax/type/(?P<type_id>\d+)/$', get_type_default),
    (r'^info/(?P<activity_id>\d+)/$', info),
    (r'^calendar/$', get_calendar),
    (r'^selectTime/$', select_time),
    
    (r'^friend-candidates/(?P<activity_id>\d+)/$', get_friend_candidates),
    (r'^potential-candidates/(?P<activity_id>\d+)/$', get_potential_candidates),
    (r'invitebymail/$', invite_by_mail)
    
#    (r'change/$', change_state)
)
