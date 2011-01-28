from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^edit/(?P<story_id>\d+)/$', 'story.views.edit'),
    (r'^detail/(?P<story_id>\d+)/$', 'story.views.detail'),
    (r'^invite/(?P<story_id>\d+)/$', 'story.views.invite'),
    (r'^candidate-pan/(?P<story_id>\d+)/$', get_candidate_pan),
    (r'^participants/(?P<story_id>\d+)/$', get_participants),
    (r'^agree/(?P<invite_id>\d+)/$', 'story.views.agree'),
    (r'^ignore/(?P<invite_id>\d+)/$', 'story.views.ignore'),
    (r'^create/$', 'story.views.create'),
    (r'^home/$', home),
    (r'^uploadphoto/(?P<story_id>\d+)/$', 'story.views.upload_photo'),
    (r'^post/(?P<story_id>\d+)/$', 'story.views.post'),
)