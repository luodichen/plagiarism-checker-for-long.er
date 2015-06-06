from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from pc_site import settings
from module import data
from module import utils
import auth
import json

# Create your views here.

def test(request):
    return HttpResponse("Hello~")

def login(request):
    result = {}
    
    user = request.REQUEST.get('user')
    password = request.REQUEST.get('password')
    
    login_state = auth.user_auth(user, password)
    result['result'] = login_state
    
    if login_state:
        auth.set_login(request)
    
    return HttpResponse(json.dumps(result), content_type = "application/json")

def logout(request):
    auth.set_logout(request)
    request_redirect = request.REQUEST.get('redirect')
    if None == request_redirect:
        return HttpResponse("OK")
    else:
        return HttpResponseRedirect(request_redirect)

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

def reportmeta(request):
    ret = {'error' : 0}
    task_id = request.REQUEST.get("id")
    title = request.REQUEST.get("title")
    author = request.REQUEST.get("author")
    metadata = request.REQUEST.get("metadata")
    
    if None == task_id:
        ret['error'] = -2
        ret['error_description'] = 'bad request: task id not found'
        return HttpResponse(json.dumps(ret), content_type = "application/json")
    
    try:
        data_obj = data.Data(settings.DATA_DIR)
        data_obj.report_meta(task_id, title, author, metadata)
    except Exception, e:
        ret['error'] = -1
        print e
    
    return HttpResponse(json.dumps(ret), content_type = "application/json")

def reportprogress(request):
    ret = {'error' : 0}
    task_id = request.REQUEST.get("id")
    progress = request.REQUEST.get("progress")
    
    if None == task_id or None == progress:
        ret['error'] = 2
        ret['error_description'] = 'bad request'
        return HttpResponse(json.dumps(ret), content_type = "application/json")
    
    try:
        data_obj = data.Data(settings.DATA_DIR)
        data_obj.report_progress(task_id, progress)
    except Exception, e:
        ret['error'] = -1
        print e
        
    return HttpResponse(json.dumps(ret), content_type = "application/json")

def reportresult(request):
    ret = {'error' : 0}
    task_id = request.REQUEST.get("id")
    result = request.REQUEST.get("result")
    result_meta = request.REQUEST.get("resultmeta")
    
    if None == task_id:
        ret['error'] = 2
        ret['error_description'] = 'bad request'
        return HttpResponse(json.dumps(ret), content_type = "application/json")
    
    try:
        data_obj = data.Data(settings.DATA_DIR)
        data_obj.report_result(task_id, result, result_meta)
    except Exception, e:
        ret['error'] = -1
        print e
        
    return HttpResponse(json.dumps(ret), content_type = "application/json")

def querylist(request):
    ret = {'error' : 0}
    
    try:
        data_obj = data.Data(settings.DATA_DIR)
        ret['result'] = data_obj.query_list(None)
    except Exception, e:
        ret['error'] = -1
        print e
        
    return HttpResponse(json.dumps(ret), content_type = "application/json")
    