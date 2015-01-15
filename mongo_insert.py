#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import timeit
import threading

from modules import csv_io
from modules import json_io
from db.Mongo import Mongo

class Pthread (threading.Thread):

    def __init__(self, thread_id, user_id, data_path, db_config):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.user_id = user_id
        self.data_path = data_path
        self.db_config = db_config

    def run(self):
        insert(self.db_config, self.data_path, self.user_id)

def get_data(file_name, included_cols=[0,1,5,6]):
    f = open(file_name)
    reader = f.readlines()[6:]
    data = []
    for row in reader:
        content = list(row.split(',')[i] for i in included_cols)
        content[-1] = content[-1][:-2]
        data.append(content)
    f.close()
    return data

def insert(db_config, data_path, user):
    mongo = Mongo()
    colle_name = db_config['collename']
    mydb = mongo.get_db(db_config['dbname'])
    for root, _, files in os.walk(data_path+user):
        for f in files:
            if f != '.DS_Store':
                data = get_data(root+'/'+f)
                for item in data:
                    item = { 
                             "user": user,
                             "lat": item[0],
                             "lng": item[1],
                             "date": item[2],
                             "time": item[3]
                           }
                    mongo.insert_doc(mydb, colle_name, item)


if __name__=='__main__':
    config = json_io.read_json('config.json')
    db_config = config[u'mongo']

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
