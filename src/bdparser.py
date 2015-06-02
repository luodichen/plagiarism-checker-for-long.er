# encoding=utf-8
'''
Created on Jun 2, 2015

@author: luodichen
'''

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2
import urllib
from pyquery import PyQuery

def parse_baidu_link(url):
    return urllib2.urlopen(url).geturl()

def get_result(keywords):
    ret = []
    url = "http://www.baidu.com/s?wd=" + keywords
    pq_baidu = PyQuery(url)
    match = pq_baidu("#container div[class^='result'] h3[class='t'] a")
    count = match.size()
    
    for i in range(0, count):
        try:
            ret.append(parse_baidu_link(match.eq(i).attr("href")))
        except:
            pass
        
    return ret
    
