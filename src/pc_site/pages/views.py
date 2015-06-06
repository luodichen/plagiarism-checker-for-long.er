'''
Created on Jun 6, 2015

@author: luodichen
'''

from django.template import Context, loader
from django.http.response import HttpResponse

def main(request):
    t = loader.get_template("main.html")
    c = Context({

    })
    return HttpResponse(t.render(c))
