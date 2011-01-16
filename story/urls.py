from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^edit/(?P<story_id>\d+)/$', 'story.views.edit'),
    (r'^detail/(?P<story_id>\d+)/$', 'story.views.detail'),
    (r'^create/$', 'story.views.create'),
)