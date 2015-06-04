'''
Created on Jun 3, 2015

@author: luodichen
'''

import threading
import sqlite3
import time

g_mutex = threading.Lock()
g_processing_timeout = 300

class Data(object):
    def __init__(self, dbfile):
        self.db = dbfile
        self.conn = sqlite3.connect(dbfile)
        self.create()
        
    @staticmethod
    def dict_fetchone(cursor):
        result = cursor.fetchone()
        if None == result:
            return None
        else:
            desc = (x[0] for x in cursor.description)
            return dict(zip(desc, result))
    
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
        ret = None
        sql_query = '''SELECT * FROM pcdata WHERE status = 0 
                        ORDER BY create_time LIMIT 0, 1'''
        sql_update = '''UPDATE pcdata SET status = ?, update_time = ?
                        WHERE _id = ?'''
        
        try:
            g_mutex.acquire(1)
            
            cursor = self.conn.cursor()
            cursor.execute(sql_query)
            ret = self.dict_fetchone(cursor)
            
            if None != ret:
                update_param = (1, int(time.time()), ret['_id'])
                cursor.execute(sql_update, update_param)
                self.conn.commit()
            
        except Exception, e:
            raise e
        finally:
            g_mutex.release()
        
        return ret
    
    def report_progress(self, task_id, process):
        sql = '''UPDATE pcdata SET status = ?, update_time = ?, completion = ?
                 WHERE _id = ?'''
        params = (1, int(time.time()), process, task_id)
        self.conn.cursor().execute(sql, params)
        self.conn.commit()
        
    def report_meta(self, task_id, title, author, meta_data):
        sql = '''UPDATE pcdata SET status = ?, update_time = ?, title = ?,
                author = ?, meta_data = ?
                WHERE _id = ?'''
        params = (1, int(time.time()), title, author, meta_data, task_id)
        self.conn.cursor().execute(sql, params)
        self.conn.commit()
    
    def report_result(self, task_id, result, result_meta):
        sql = '''UPDATE pcdata SET status = ?, update_time = ?, result = ?,
                result_meta = ?, completion = ?
                WHERE _id = ?'''
        params = (2, int(time.time()), result, result_meta, 100, task_id)
        self.conn.cursor().execute(sql, params)
        self.conn.commit()

    def url_exists(self, url):
        sql = '''SELECT COUNT(*) FROM pcdata WHERE url = ?'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (url, ))
        
        return cursor.fetchone()[0] > 0
    
    def restore_timedout_task(self):
        sql = '''UPDATE pcdata SET status = ? 
                WHERE status = 1 AND update_time < ?'''
        params = (0, int(time.time()) - g_processing_timeout, )
        self.conn.cursor().execute(sql, params)
        self.conn.commit()
    
