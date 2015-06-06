# encoding=utf-8
'''
Created on Jun 2, 2015

@author: luodichen
'''

import string
import content
import bdparser
import utils

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

def analysis(url, choise = 3, progress_callback = None, meta_callback = None):
    article_meta = content.get_article_meta(url)
    
    if None != meta_callback:
        meta_callback(article_meta)
    
    article_content = pre_process(article_meta['content'])
    keywords = get_keywords(article_content, choise)
    
    totalpart = 0
    match_set = set()
    details = []
    
    kw_index = -1
    kw_length = len(keywords)
    for kw in keywords: 
        kw_index = kw_index + 1
        try:
            match_urls = bdparser.get_result(kw)
        except:
            continue
        
        match_index = -1
        match_length = len(match_urls)
        for match_url in match_urls:
            match_index = match_index + 1
            try:
                reference, ref_url = content.get_text(match_url)
                
                if utils.regular_url(url) != None and utils.regular_url(url) == utils.regular_url(ref_url):
                    continue
                
                match_text = pre_process(reference)
                _, totalpart, cur_set = text_match(article_content, match_text)
                match_set.update(cur_set)
                details.append((ref_url, list(cur_set), ))

                if None != progress_callback:
                    progress = 10 + 80 * kw_index / kw_length + (80 / kw_length) * match_index / match_length
                    progress_callback(progress, ref_url)
            except:
                continue
    
    return totalpart, list(match_set), details
