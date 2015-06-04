'''
Created on Jun 4, 2015

@author: luodichen
'''

from django.conf.urls import url

urlpatterns = [
    url(r'^test/$', 'api.views.test'),
    url(r'^addtask/$', 'api.views.addtask'),
]