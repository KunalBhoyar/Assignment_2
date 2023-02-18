
import boto3
from dotenv import dotenv_values
import string
import time

config = dotenv_values(".env")   

def geos_query_files(product, year, day, hour):

    s3client = boto3.client('s3',
                        region_name='us-east-1')

    # prefix = product + "/" + str(year) + "/" + str(day) + "/" + str(hour)
    prefix = product + "/" + str(year) + "/" + str(day) + "/" + str(hour)

    print(prefix)

    response = s3client.list_objects_v2(Bucket="noaa-goes18", Prefix = prefix )
    contents = response.get("Contents")
    
    files = []

    for content in contents:
        # print(content['Key'])
        files.append(content['Key'])
        # files.append(content['Key'].split("/")[-1])

    return files


def downloadFileAndMove(fileName):
    print("FileName", fileName)
    session = boto3.Session(
        aws_access_key_id = config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
    )
    
    s3 = session.resource('s3')

    copy_source = {
        'Bucket': "noaa-goes18",
        'Key': fileName
    }

    bucket = s3.Bucket('damg7245-s3-storage')
    
    bucket.copy(copy_source, fileName)


def get_geos_file_link(filename):

    print("get_geos_file_link", filename)

    file = filename.split("_")

    # prefix = "https://noaa-goes18.s3.amazonaws.com/"
    product = '-'.join(file[1].split("-")[:-1]).rstrip(string.digits)
    year = file[3][1:5]
    day = file[3][5:8]
    hour = file[3][8:10]

    file_prefix =  product + "/" + year + "/" + day + "/" + hour + "/" + filename

    print("*****************************", file_prefix)

    downloadFileAndMove(file_prefix)

    return file_prefix


### NEXRAD AWS S3 Utils

def nexrad_query_files(year, month, day, site):

    source_bucket_name = "noaa-nexrad-level2"

    s3client = boto3.client('s3',
                        region_name='us-east-1')

    # prefix = product + "/" + str(year) + "/" + str(day) + "/" + str(hour)
    prefix = str(year) + "/" + str(month) + "/" + str(day) + "/" + str(site)

    print(prefix)

    response = s3client.list_objects_v2(Bucket = source_bucket_name, Prefix = prefix )
    contents = response.get("Contents")
    
    files = []

    for content in contents:
        print(content['Key'])
        files.append(content['Key'])
        # files.append(content['Key'].split("/")[-1])

    return files


def copyFileFromNexradToS3(fileName):
    
    source_bucket_name = "noaa-nexrad-level2"

    session = boto3.Session(
        aws_access_key_id = config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
    )
    
    s3 = session.resource('s3')

    copy_source = {
        'Bucket': source_bucket_name,
        'Key': fileName
    }

    bucket = s3.Bucket('damg7245-s3-storage')
    
    bucket.copy(copy_source, fileName)


def get_nexrad_file_link(filename):
    file = filename.split("_")

    site = file[0][:4]
    year = file[0][4:8]
    month = file[0][8:10]
    day = file[0][10:12]

    file_prefix =  year + "/" + month + "/" + day + "/" + site + "/" + filename

    copyFileFromNexradToS3(file_prefix)

    return file_prefix


##### Cloudwatch Logs

# cloudwatch = boto3.client('logs', 
#     aws_access_key_id = config["AWS_ACCESS_KEY_ID"],
#     aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"],
#     region_name='us-east-1'
# )

def getCloudwatchInstance():
    cloudwatch = boto3.client('logs', 
        aws_access_key_id = config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"],
        region_name='us-east-1'
    )
    return cloudwatch

def create_steamlit_logs(cloudwatch, msg):
    cloudwatch.put_log_events(
        logGroupName= config["LOG_GROUP_NAME"],
        logStreamName= config["LOG_STREAMLIT_NAME"],
        logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': msg
                },
            ]
    )