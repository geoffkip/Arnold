#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 22:55:58 2018

@author: geoffrey.kip
"""

from os import chdir
import pandas as pd
import  sqlite3
from datetime import datetime

# Set working directory
wd="/Users/geoffrey.kip/Projects"
chdir(wd)


#create database
database = "/Users/geoffrey.kip/Projects/Arnold/data_collector.db"
db = sqlite3.connect(database)
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE data_collector(
               user text,
               text_body TEXT,
               recorded_at DATETIME
              )
''')
db.commit()

current_date= datetime.now().strftime("%Y-%m-%d")
user= "Geoffrey Kip"
text= "I need to know a good place to find narxan"

cursor.execute('''INSERT INTO data_collector(user, text_body, recorded_at)
                  VALUES(?,?,?)''', (user,text,current_date))
db.commit()

df = pd.read_sql_query("select * from data_collector;", db)

def collect_data(user=None, data=None):
    user= user
    date= datetime.now().strftime("%Y-%m-%d")
    data= data
    database = "./data_collector.db"
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO data_collector(user, text_body, recorded_at)
                  VALUES(?,?,?)''', (user,data,date))
    db.commit()

collect_data(user,text)