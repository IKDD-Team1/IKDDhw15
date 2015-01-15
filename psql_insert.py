#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import timeit
import threading

from modules import json_io
from db.MyDB import MyDB

class Pthread (threading.Thread):

    def __init__(self, thread_id, user_id, data_path, db_config):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.user_id = user_id
        self.data_path = data_path
        self.db_config = db_config

    def run(self):
        user_insert(self.db_config, self.data_path, self.user_id)

def get_data(file_name, included_cols=[0,1,5,6]):
    f = open(file_name)
    reader = f.readlines()[6:]
    data = []
    for row in reader:
        content = list(row.split(',')[i] for i in included_cols)
        data.append(content)
    f.close()
    return data

def user_insert(db_config, data_path, user, table_name='test_table'):
    mydb = MyDB(db_config[u'dbtype'], db_config[u'host'], db_config[u'dbname'], \
            db_config[u'username'], db_config[u'password'], db_config[u'encoding'], None)

    for root, _, files in os.walk(data_path+user):
        for f in files:
            if f != '.DS_Store':
                data = get_data(root+'/'+f)
                for item in data:
                    item.insert(0, user)
                    mydb.insert(table_name, ['user_id', 'latitude', \
                           'longitude', 'date', 'time'], item)
    mydb.commit()
    mydb.close()



if __name__=='__main__':
    config = json_io.read_json('config.json')
    db_config = config[u'database']
    table_name = config[u'table']

    threads = []
    start = timeit.default_timer()

    for i in range(0, 6):
        thread = Pthread('Thread-'+str(i), '00'+str(i), \
                config[u'data'][u'folder_path'], db_config)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    stop = timeit.default_timer()
    print 'Time:', (stop - start), 's'
