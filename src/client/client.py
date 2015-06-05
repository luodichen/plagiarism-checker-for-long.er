'''
Created on Jun 5, 2015

@author: luodichen
'''

import urllib2
import json
import time
import analysis
from urllib import urlencode

API_URL = "http://localhost:8000/api"

def quest_task():
    ret = None
    url = API_URL + "/questtask/"
    
    try:
        result = json.loads(urllib2.urlopen(url).read())
        if 0 == result['error']:
            ret = result['result']
            
    except Exception, e:
        print e
        
    return ret

def report_progress(task_id, progress):
    url = API_URL + "/report/progress/"
    data = {'id' : task_id, 'progress' : progress}
    
    try:
        urllib2.urlopen(url, urlencode(data)).read()
    except:
        pass
    
def report_result(task_id, result, resultmeta):
    url = API_URL + "/report/result/"
    data = {'id' : task_id, 'result' : result, 'resultmeta' : resultmeta}
    
    try:
        response = json.loads(urllib2.urlopen(url, urlencode(data)).read())
    except Exception, e:
        print e
        return -1
    
    return response['error']

def main():
    while True:
        try:
            task =  quest_task()
            if None == task:
                print "no more task now, waiting for 10 seconds......"
                time.sleep(10)
                continue
            
            url = task['url']
            print "new task " + url
            prev_progress_val = 0
            
            def progress(val, url):
                print "%d%% checked - %s" % (val, url)
                #print prev_progress_val
                #if val - prev_progress_val > 20:
                #    report_progress(task['_id'], val)
                #    prev_progress_val = val
                #    print "report progress %d" % (val, )
            
            totalpart, match_set, details = analysis.analysis(url, progress_callback = progress)
            result = 100 * len(match_set) / totalpart
            print "completed. result = %d%%" % (result, )
            print "reporting to server......"
            report_ret = report_result(task['_id'], result, json.dumps(details))
            if 0 == report_ret:
                print "ok."
            else:
                print "failed - %d" % (report_ret, )
            
        except Exception, e:
            print e
            print "waiting for 30 seconds......"
            time.sleep(30)
            continue
    
main()
