from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^register/$', "accounts.views.register"),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^ajax/checkuser/(?P<email>\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)/$', check_user_exist),#email regex
)

