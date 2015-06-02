'''
Created on Jun 2, 2015

@author: luodichen
'''

from pyquery import PyQuery
import urllib2
import re

def remove_html_label(original):
    r = re.compile(r'<[^>]+>', re.S)
    return r.sub('', original)

def get_text(url):
    original = urllib2.urlopen(url).read()
    return remove_html_label(original)

def get_article_meta(url):
    ret = {}
    pq = PyQuery(url)
    r_meta = re.compile(r'<strong.+</strong>', re.S)
    
    ret['title'] = pq("div[class='shows'] h1").html()
    metadata = pq("table[class='yss'] td")
    ret['publish'] = r_meta.sub('', metadata.eq(0).html()).strip()
    ret['publish_date'] = r_meta.sub('', metadata.eq(1).html()).strip()
    ret['submit'] = r_meta.sub('', metadata.eq(2).html()).strip()
    ret['submit_date'] = r_meta.sub('', metadata.eq(3).html()).strip()
    
    content = pq("div[class='show'] table tr")
    ret['article'] = content.eq(0).children("td").eq(1).text()
    ret['content'] = content.eq(1).children("td").eq(1).text()
    
    return ret

result =  get_article_meta("http://training.hnteacher.net/Elearning/ClassPortal/GoodHomeworkDetail.aspx?ID=531639&CLASS_ID=4300000000f16&Tatget=")
print result['title']
print result['publish']
print result['publish_date']
print result['submit']
print result['submit_date']
print result['article']
print result['content']
