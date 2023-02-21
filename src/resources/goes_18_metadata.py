import os
import boto3
import logging
from dotenv import load_dotenv
import csv
from csv import writer
import sqlite3
import pandas as pd


load_dotenv() #loads all environment variables from .env file 

#DB connection
conn = sqlite3.connect('src/data/GEOSPATIAL_DATA.db')
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS goes18meta''')
c.execute('''CREATE TABLE goes18meta
                   (year INTEGER, month INTEGER, hour INTEGER)''')


# #establishing connection to s3 using boto3
s3client = boto3.client('s3',region_name='us-east-1')
bucket = "noaa-goes18"
def get_folders(bucket, prefix):
    result = s3client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    if "CommonPrefixes" in result:
        return [prefix + "/" + prefixes['Prefix'] for prefixes in result["CommonPrefixes"]]
    return []

def scrape_data(bucket,prefix):
    sub_folder=get_folders(bucket,prefix)
    if len(sub_folder) != 0:
        for folder in sub_folder:
            name_folder=folder.split('//')[1]
            scrape_data(bucket,name_folder)
            if len(get_folders(bucket,name_folder)) == 0:
                val=folder.split('//')[1].split('/')
                c.execute("INSERT INTO goes18meta (year, month, hour) VALUES (?,?,?)", (val[1], val[2], val[3]))
                print(val[1],val[2],val[3])


scrape_data(bucket=bucket,prefix="ABI-L1b-RadC/")
conn.commit()
conn.close()


