#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:37:41 2018

@author: geoffrey.kip
"""
# Import required packages
from os import chdir
import pandas as pd
import  sqlite3

# Set working directory
wd="/Users/geoffrey.kip/Projects"
chdir(wd)


#create database
database = "/Users/geoffrey.kip/Projects/Arnold/facilities.db"
db = sqlite3.connect(database)
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE facilities(
               name_of_doctor text,
               type_of_clinic TEXT,
               street1 TEXT,
               street2 TEXT
               city,
               state TEXT,
               zip INTEGER,
               zip4 INTEGER,
               county TEXT ,
               phone INTEGER,
               intake_prompt TEXT,
               intake1 TEXT,
               intake2 TEXT,
               website TEXT,
               latitude FLOAT,
               longitude FLOAT,
               type_facility TEXT,
               last_update DATETIME
              )
''')
db.commit()


df= pd.read_csv("facilities.csv")
df.to_sql("facilities",con=db, if_exists="replace")

def return_facilities(zipcode=None):
        data=[]
        database = "/Users/geoffrey.kip/Projects/Arnold/facilities.db"
        db = sqlite3.connect(database)
        cursor= db.cursor()
        sql="""SELECT * FROM (SELECT
        name_of_doctor || " " || street1 || " " ||  street2 || " " || city ||  " " || state || " " || zip || " " ||  phone as address
        FROM facilities where zip={0}) where address is not null""".format(zipcode)
        result = cursor.execute(sql)
        for row in result:
            data.append(row)
        return str(data)

data= return_facilities(19104)
    
