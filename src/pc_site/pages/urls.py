'''
Created on Jun 6, 2015

@author: luodichen
'''

from django.conf.urls import url

urlpatterns = [
    url(r'^main/$', 'pages.views.main'),
    url(r'^login/$', 'pages.views.login'),
]