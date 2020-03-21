import logging
import boto3
from botocore.exceptions import ClientError

class s3_client():
    username = None
    s3_client = None

    def __init__(self, username):
        self.username = username
        self.s3_client = boto3.client('s3')

    def list_buckets(self):
        # Retrieve the list of existing buckets
        response = self.s3_client.list_buckets()
        
        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def create_bucket(self, bucket_name):
        # Create bucket
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, bucket, 
                                                  self.username + '/media/' + object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    def getuserfiles(self, bucketname):
        # Upload the file
        mybucket = self.s3_client.get_bucket(bucketname)
        keys = mybucket.list(self.username)
        totalsize=0.0
        userfiles = {}
        for key in keys:
            value=[]
            #value.append(key.name)
            filename = key.name
            filename=filename.replace(self.username+'/media/','')
            value.append(key.last_modified)
            keysize = float(key.size)/1000.0
            value.append(str(keysize))
            userfiles[filename]=value
            totalsize = totalsize + float(key.size)
        totalsize = totalsize/1000000.0
        return userfiles,totalsize

    def delete_from_s3(self, bucketname, filename):
        # Upload the file
        mybucket = self.s3_client.get_bucket(bucketname)
        mybucket.delete_key(self.username+'/media/'+filename)

