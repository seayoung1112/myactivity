from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^edit/(?P<story_id>\d+)/$', 'story.views.edit'),
    (r'^detail/(?P<story_id>\d+)/$', 'story.views.detail'),
    (r'^invite/(?P<story_id>\d+)/$', 'story.views.invite'),
    (r'^agree/(?P<invite_id>\d+)/$', 'story.views.agree'),
    (r'^ignore/(?P<invite_id>\d+)/$', 'story.views.ignore'),
    (r'^create/$', 'story.views.create'),
    (r'^uploadphoto/(?P<story_id>\d+)/$', 'story.views.upload_photo'),
    (r'^post/(?P<story_id>\d+)/$', 'story.views.post'),
)