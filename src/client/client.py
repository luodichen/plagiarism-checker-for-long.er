'''
Created on Jun 5, 2015

@author: luodichen
'''

import urllib2
import json
import time
import analysis
import sys
from urllib import urlencode

global API_URL
API_URL = None

def quest_task():
    global API_URL
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
    global API_URL
    url = API_URL + "/report/progress/"
    data = {'id' : task_id, 'progress' : progress}
    
    try:
        urllib2.urlopen(url, urlencode(data)).read()
    except:
        pass
    
def report_result(task_id, result, resultmeta):
    global API_URL
    url = API_URL + "/report/result/"
    data = {'id' : task_id, 'result' : result, 'resultmeta' : resultmeta}
    
    try:
        response = json.loads(urllib2.urlopen(url, urlencode(data)).read())
    except Exception, e:
        print e
        return -1
    
    return response['error']

def report_meta(task_id, metadata):
    global API_URL
    url = API_URL + "/report/meta/"
    data = {'id' : task_id, 'title' : metadata['title'], 
            'author' : metadata['submit'], 'metadata' : json.dumps(metadata)}
    
    try:
        response = json.loads(urllib2.urlopen(url, urlencode(data)).read())
    except Exception, e:
        print e
        return -1
    
    return response['error']

def main(argv):
    global API_URL
    API_URL = argv[1]
    
    print "Server: " + API_URL
        
    while True:
        try:
            task =  quest_task()
            if None == task:
                print "no more task now, waiting for 20 seconds......"
                time.sleep(20)
                continue
            
            url = task['url']
            print "new task " + url
            
            def progress(val, url):
                print "%d%% checked - %s" % (val, url)
                
            def meta(metadata):
                print metadata['title']
                print "task_id = %d, reporting metadata to server......" % (task['_id'], )
                print "ok." if 0 == report_meta(task['_id'], metadata) else "failed."
            
            totalpart, match_set, details = analysis.analysis(url, progress_callback = progress, meta_callback = meta)
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
    
if __name__ == '__main__':
    main(sys.argv)
