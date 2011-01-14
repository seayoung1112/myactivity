from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', 
    (r'^search/$', 'friends.views.search'),
    (r'^add/(?P<user_id>\d+)/$', 'friends.views.add'),
    (r'^agree/(?P<app_id>\d+)/$', 'friends.views.agree'),
    (r'^ignore/(?P<app_id>\d+)/$', 'friends.views.ignore'),
    (r'^application/$', 'friends.views.application'),

)