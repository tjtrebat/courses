__author__ = 'Tom'

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^login/$', 'registration.views.user_login', name='login'),
 )
  