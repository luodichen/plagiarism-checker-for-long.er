# encoding=utf-8
'''
Created on Jun 2, 2015

@author: luodichen
'''

from pyquery import PyQuery
import urllib2
import string
import re

def remove_html_label(original):
    r = re.compile(r'<[^>]+>', re.S)
    return r.sub('', original)

def get_text(url):
    pq = PyQuery(urllib2.urlopen(url, timeout = 10).read())
    return pq("body").text()

def get_article_meta(url):
    ret = {}
    pq = PyQuery(url)
    
    if (url.lower().find("goodhomeworkdetail.aspx") != -1):
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
    elif (url.lower().find("experience_detail.aspx") != -1):
        ret['title'] = pq("div[class='shows'] h1").html()
        ret['content'] = pq("div[class='show']").text()
    
    return ret

def pre_process(original):
    char_remove = string.punctuation + string.digits + u"【】｛｝（）《》，。？、“”’‘；： \t"
    return "".join([c for c in original if c not in char_remove])
