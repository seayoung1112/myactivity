from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^activity/', include('user_activity.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'profile/', include('profile.urls')),
    (r'friends/', include('friends.urls')),
    (r'privacy/', include('privacy.urls')),
    (r'story/', include('story.urls')),
    (r'^$', 'home.views.index'),
    (r'^home/$', 'home.views.home'),    
    (r'^suggest/$', 'home.views.suggest'),
    (r'^about/$', 'home.views.about'),
    (r'^updates/$', 'home.views.updates'),
    (r'^contact/$', 'home.views.contact'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),)