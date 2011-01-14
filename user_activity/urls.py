from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from models import ActivityType

urlpatterns = patterns('',
    (r'^create/$', 'user_activity.views.create'),
    (r'^createtype/$', 'user_activity.views.create_type'),
    (r'^detail/(?P<activity_id>\d+)/$', 'user_activity.views.detail'),
    (r'^edit/(?P<activity_id>\d+)/$', 'user_activity.views.edit'),
    (r'^reply/(?P<activity_id>\d+)/$', 'user_activity.views.reply'),
    (r'^invite/(?P<activity_id>\d+)/$', 'user_activity.views.invite'),
    (r'^setdefault/$', 'user_activity.views.set_type_default'),
    (r'^ajax/type/(?P<type_id>\d+)/$', 'user_activity.views.get_type_default'),
)
