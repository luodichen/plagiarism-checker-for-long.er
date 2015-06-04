from django.shortcuts import render
from django.http.response import HttpResponse
from pc_site import settings
from module import data
from module import utils
import json

# Create your views here.

def test(request):
    return HttpResponse("Hello~")

def addtask(request):
    ret = {'error' : 0}
    
    try:
        url = utils.regular_url(request.REQUEST.get('url'))
        if None == url:
            ret['error'] = -2
            ret['error_description'] = 'url not passed'
        else:
            data_obj = data.Data(settings.DATA_DIR)
            if data_obj.url_exists(url):
                ret['error'] = -3
                ret['error_description'] = 'url exists'
            else:
                data_obj.add_task(url)
    except Exception, e:
        ret['error'] = -1
        print e
        
    return HttpResponse(json.dumps(ret), content_type = "application/json")

def questtask(request):
    ret = {'error' : 0}
    
    try:
        data.Data(settings.DATA_DIR).restore_timedout_task()
    except:
        pass
    
    try:
        data_obj = data.Data(settings.DATA_DIR)
        result = data_obj.request_task()
        ret['result'] = result
    except Exception, e:
        ret['error'] = -1
        print e
    
    return HttpResponse(json.dumps(ret), content_type = "application/json")
    