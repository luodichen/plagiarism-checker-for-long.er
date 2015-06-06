'''
Created on Jun 4, 2015

@author: luodichen
'''

from django.conf.urls import url

urlpatterns = [
    url(r'^test/$', 'api.views.test'),
    url(r'^addtask/$', 'api.views.addtask'),
    url(r'^questtask/$', 'api.views.questtask'),
    url(r'^report/meta/$', 'api.views.reportmeta'),
    url(r'^report/progress/$', 'api.views.reportprogress'),
    url(r'^report/result/$', 'api.views.reportresult'),
    url(r'^query/list/$', 'api.views.querylist'),
    url(r'login/$', 'api.views.login'),
    url(r'logout/$', 'api.views.logout'),
]
