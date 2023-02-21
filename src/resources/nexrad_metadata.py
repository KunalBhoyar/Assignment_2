import os
import boto3
import logging
from dotenv import load_dotenv
import csv
from csv import writer
import sqlite3
import time


load_dotenv() #loads all environment variables from .env file 


#Define the AWS access key and secret
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
logGroupName=os.environ.get('LOG_GROUP_NAME')
logStreamName=os.environ.get('LOG_STREAM_NAME')

#Create an S3 client using the access key and secret
def init_resources():
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
    )
    cloudwatch = boto3.client('logs', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1')
    return cloudwatch,s3


def creat_logs(cloudwatch,msg):
    cloudwatch.put_log_events(
                logGroupName=logGroupName,
                logStreamName=logStreamName,
                logEvents=[
                        {
                            'timestamp': int(time.time() * 1000),
                            'message': msg
                        },
                    ]
            )



conn = sqlite3.connect('src/data/GEOSPATIAL_DATA.db')
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS nexradmeta''')
c.execute('''CREATE TABLE nexradmeta
                   (year INTEGER, month INTEGER, hour INTEGER, stationcode TEXT)''')

s3client = boto3.client('s3',region_name='us-east-1')
bucket = "noaa-nexrad-level2"

operation_parameters_2022 = {'Bucket': 'noaa-nexrad-level2',
                        'Prefix': '2022/'}
operation_parameters_2023 = {'Bucket': 'noaa-nexrad-level2',
                        'Prefix': '2023/'}
paginator = s3client.get_paginator('list_objects_v2')
pages_2022 = paginator.paginate(**operation_parameters_2022)
pages_2023 = paginator.paginate(**operation_parameters_2023)


cloudwatch,s3=init_resources()

try:
    for page in pages_2022:
        # for obj in page['Contents']:
        #     print(obj)
        for content in page.get("Contents"):
            # print(content.get("Key"))
            val = content.get("Key").split("/")
            print(val)
            c.execute("INSERT INTO nexradmeta (year, month, hour, stationcode) VALUES (?,?,?,?)", (val[0], val[1], val[2], val[3]))
                
    creat_logs(cloudwatch=cloudwatch,msg="Data Dumped to nexrad-2022 database")
    
except Exception as e:
    creat_logs(cloudwatch=cloudwatch,msg="Exception "+str(e))


try:
    for page in pages_2023:
        # for obj in page['Contents']:
        #     print(obj)
        for content in page.get("Contents"):
            # print(content.get("Key"))
            val = content.get("Key").split("/")
            print(val)
            c.execute("INSERT INTO nexradmeta (year, month, hour, stationcode) VALUES (?,?,?,?)", (val[0], val[1], val[2], val[3]))
    creat_logs(cloudwatch=cloudwatch,msg="Data Dumped to nexrad-2023 database")
            
except Exception as e:
    creat_logs(cloudwatch=cloudwatch,msg="Exception "+str(e))
            
            
conn.commit()
conn.close()