import boto3
import time
from dotenv import load_dotenv
import os
import string


class s3_copy():
    def __init__(self):
        #loading env variables
        load_dotenv()
        # Define the AWS access key and secret
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.logGroupName=os.environ.get('LOG_GROUP_NAME')
        self.logStreamName=os.environ.get('LOG_STREAM_NAME_AWS')
        self.bucket_name=os.environ.get('BUCKET_NAME')
    # Create an S3 client using the access key and secret
    def init_resources(self):
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='us-east-1'
        )
        cloudwatch = boto3.client('logs', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='us-east-1')
        return cloudwatch,s3

    def create_AWS_logs(self,msg):
        cloudwatch = self.init_resources()
        cloudwatch.put_log_events(
                    logGroupName=self.logGroupName,
                    logStreamName=self.logStreamName,
                    logEvents=[
                            {
                                'timestamp': int(time.time() * 1000),
                                'message': msg
                            },
                        ]
                )
    # Write a file to an S3 bucket
    def copy_file_into_s3(self,source_bucket,key):
        cloudwatch,s3=self.init_resources()
        copy_source = {
            'Bucket': source_bucket,
            'Key': key
            }
        try:  
            bucket = s3.Bucket(self.bucket_name)
            bucket.copy(copy_source, key)
            self.creat_logs(cloudwatch=cloudwatch,msg="Copy success for file: "+ str(key))
            return True
        except Exception as e:
            self.creat_logs(cloudwatch=cloudwatch,msg="Exception "+ str(e))
            return False
    
    #copy file from goes public bucket
    def downloadFileAndMove(self, source_bucketName, fileName, AWS_ACCESS_KEY_ID ,AWS_SECRET_ACCESS_KEY):
        print("FileName", fileName, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        try:
            session = boto3.Session(
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )
            
            s3 = session.resource('s3')

            copy_source = {
                'Bucket': source_bucketName,
                'Key': fileName
            }

            bucket = s3.Bucket('damg7245-s3-storage')
            
            bucket.copy(copy_source, fileName)
            return True
        except Exception as e:
            print(e)
            return False

    #search by filename
    def get_geos_file_link(self, filename, AWS_ACCESS_KEY_ID ,AWS_SECRET_ACCESS_KEY):

        # print("get_geos_file_link", filename)

        try:
            file = filename.split("_")
            print(file)
            # prefix = "https://noaa-goes18.s3.amazonaws.com/"
            product = '-'.join(file[1].split("-")[:-1]).rstrip(string.digits)
            year = file[3][1:5]
            day = file[3][5:8]
            hour = file[3][8:10]

            file_prefix =  product + "/" + year + "/" + day + "/" + hour + "/" + filename

            # print("*****************************", file_prefix)

            goesFileStatus = self.downloadFileAndMove("noaa-goes18", file_prefix, AWS_ACCESS_KEY_ID ,AWS_SECRET_ACCESS_KEY)
            print(goesFileStatus)
            if goesFileStatus:
                return {"file_prefix": file_prefix}
            return False
        
        except:
            return False
        
    def nexrad_query_files(self, year, month, day, site):

        # print(year, month, day, site)

        try:
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
                # files.append(content['Key'])
                files.append(content['Key'].split("/")[-1])

            return files
        
        except:
            print("Bucket or files not found")

    def get_nexrad_file_link(self, filename, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
        try:
            source_bucket_name = "noaa-nexrad-level2"
            file = filename.split("_")

            site = file[0][:4]
            year = file[0][4:8]
            month = file[0][8:10]
            day = file[0][10:12]

            file_prefix =  year + "/" + month + "/" + day + "/" + site + "/" + filename

            fileStatus = self.downloadFileAndMove(source_bucket_name, file_prefix, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

            if fileStatus:
                return file_prefix
            
            return fileStatus
        
        except:
            return False
