from django.conf.urls.defaults import *
import settings
from views import *


urlpatterns = patterns('',
    (r'^inbox/', inbox),
    (r'^sended/', sended),
    (r'^send/', send),
)