from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('', 
    (r'^add/(?P<user_id>\d+)/$', 'friends.views.add'),
    (r'^agree/(?P<app_id>\d+)/$', 'friends.views.agree'),
    (r'^ignore/(?P<app_id>\d+)/$', 'friends.views.ignore'),
    (r'^invitation/$', 'friends.views.invitation'),

)