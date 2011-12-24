__author__ = 'Tom'

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^tests/$', 'student.views.test_list', name='tests'),
)