from django.conf.urls.defaults import *
from views import *
from django.contrib.auth.views import *

urlpatterns = patterns('',
    (r'^register/$', "accounts.views.register"),
    (r'^login/$', 'accounts.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^changepassword/$', password_change),
    (r'^forgetPassword/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/reset_password.html',
                                                                        'email_template_name': 'accounts/reset_password_email.html',
                                                                        'post_reset_redirect': '/accounts/resetDone',
                                                                        'is_admin_site': True,},),
    (r'^resetDone/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/reset_password_done.html'}),
    (r'^resetPassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'accounts/reset_confirm.html',
                                                                          'post_reset_redirect': '/'}),                                                        
    (r'^ajax/checkuser/(?P<email>\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)/$', check_user_exist),#email regex
)

