'''
Created on Jun 5, 2015

@author: luodichen
'''


from urlparse import urlparse, parse_qs

def regular_url(url_str):
    url_str = url_str.lower()
    if url_str.find("hnteacher.net") == -1:
        return None
    
    pr = urlparse(url_str)
    id = parse_qs(pr.query)['id'][0].strip()
    class_id = parse_qs(pr.query)['class_id'][0].strip()
    
    return pr.scheme + "://" + pr.netloc + pr.path + "?id=" + id + "&class_id=" + class_id

