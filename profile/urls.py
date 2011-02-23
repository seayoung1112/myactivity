from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^edit/$', 'profile.views.edit'),
    (r'edittags/$', edit_tags),
    (r'^addtag/$', 'profile.views.add_tag'),
    (r'^removetag/(?P<tag_id>\d+)/$', 'profile.views.remove_tag'),
    (r'^addtag/(?P<tag_id>\d+)/$', 'profile.views.add_tag'),
)