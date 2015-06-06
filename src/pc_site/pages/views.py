'''
Created on Jun 6, 2015

@author: luodichen
'''

from django.template import Context, loader
from django.http.response import HttpResponse, HttpResponseRedirect
from api import auth

def main(request):
    if not auth.check_login(request):
        return HttpResponseRedirect(r'/pages/login/')
    
    t = loader.get_template("main.html")
    c = Context({

    })
    return HttpResponse(t.render(c))

def login(request):
    if auth.check_login(request):
        return HttpResponseRedirect(r'/pages/main/')
    
    t = loader.get_template("login.html")
    c = Context({
        'login_url':r'/api/login/',
        'on_success':r'/pages/main/',
    })
    return HttpResponse(t.render(c))

def index(request):
    return HttpResponseRedirect(r'/pages/main/')
