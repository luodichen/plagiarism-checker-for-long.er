# encoding=utf-8
'''
Created on Jun 2, 2015

@author: luodichen
'''

import string
import content
import bdparser

PART_SIZE = 12
KEYWORD_LENGTH = 36

def pre_process(original):
    char_remove = string.punctuation + string.digits + u"【】｛｝（）《》，。？、“”’‘；： \t"
    return "".join([c for c in original if c not in char_remove])

def get_keywords(content, choise):
    ret = []
    length = len(content)
    repart = choise + 2
    for i in range(1, repart):
        start = i * (length / repart)
        ret.append(content[start:(start + KEYWORD_LENGTH)])
    
    return ret

def text_match(text_from, text_to):
    matched = 0
    total = 0
    part_set = set()
    part = len(text_from) / PART_SIZE
    for i in range(0, part):
        if text_to.find(text_from[PART_SIZE * i:(PART_SIZE * i + PART_SIZE)]) != -1:
            matched = matched + 1
            part_set.add(i)
            
        total = total + 1
    
    return matched, total, part_set

def analysis(url, choise = 3):
    article_meta = content.get_article_meta(url)
    article_content = pre_process(article_meta['content'])
    keywords = get_keywords(article_content, choise)
    
    totalpart = 0
    match_set = set()
    details = []
    
    for kw in keywords: 
        try:
            match_urls = bdparser.get_result(kw)
        except:
            continue
        for match_url in match_urls:
            try:
                match_text = pre_process(content.get_text(match_url))
                _, totalpart, cur_set = text_match(article_content, match_text)
                match_set.update(cur_set)
                details.append((match_url, cur_set))
                print "%s - %d" % (match_url, 100 * _ / totalpart)
            except:
                continue
    
    return totalpart, match_set

def test():
    total, match_set = analysis("http://training.hnteacher.net/Elearning/ClassPortal/Experience_detail.aspx?ID=303812&CLASS_ID=4306000000045&Tatget=")
    print 100 * len(match_set) / total
    print match_set

test()