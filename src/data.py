'''
Created on Jun 3, 2015

@author: luodichen
'''

import threading
import sqlite3
import time

g_mutex = threading.Lock()

class Data(object):
    def __init__(self, dbfile):
        self.db = dbfile
        self.conn = sqlite3.connect(dbfile)
        self.create()
    
    def create(self):
        # status
        # 0 - waiting for processing
        # 1 - processing
        # 2 - completed
        # 3 - error
        
        sql = '''CREATE TABLE IF NOT EXISTS pcdata (
                    _id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT DEFAULT NULL,
                    author TEXT DEFAULT NULL,
                    url TEXT DEFAULT NULL,
                    create_time INTEGER DEFAULT 0,
                    update_time INTEGER DEFAULT 0,
                    meta_data TEXT DEFAULT NULL,
                    status INTEGER DEFAULT 0,
                    completion INTEGER DEFAULT 0,
                    result INTEGER DEFAULT 0,
                    result_meta TEXT DEFAULT NULL
                )'''
        self.conn.execute(sql)

    def add_task(self, url):
        sql = '''INSERT INTO pcdata (url, create_time, update_time)
                VALUES (?, ?, ?)'''
        params = (url, int(time.time()), int(time.time()))
        self.conn.execute(sql, params)
        self.conn.commit()
        
    def request_task(self):
        sql_query = '''SELECT * FROM pcdata WHERE status = 0 
                        ORDER BY create_time LIMIT 0, 1'''
        sql_update = '''UPDATE pcdata SET status = ?, update_time = ?
                        WHERE _id = ?'''
        try:
            g_mutex.acquire(1)
        except Exception, e:
            raise e
        finally:
            g_mutex.release()

def test():
    pass
    Data(r"C:\test.db").request_task()
    
test()
