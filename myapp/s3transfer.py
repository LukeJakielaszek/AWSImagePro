import logging
import boto3
import boto.s3
from botocore.exceptions import ClientError

def list_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(bucket['Name'])

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def percent_cb(complete, total):
    print ('.')

def upload_to_s3_bucket_file(bucketname, filename):
    print('uploading [' + filename + '] to [' + bucketname + ']')
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(filename, bucketname, filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
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
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def getuserfiles(bucketname,username):
    # Upload the file
    s3_client = boto3.client('s3')
    
    mybucket = conn.get_bucket(bucketname)
    keys = mybucket.list(username)
    totalsize=0.0
    userfiles = {}
    for key in keys:
        value=[]
        #value.append(key.name)
        filename = key.name
        filename=filename.replace(username+'/media/','')
        value.append(key.last_modified)
        keysize = float(key.size)/1000.0
        value.append(str(keysize))
        userfiles[filename]=value
        totalsize = totalsize + float(key.size)
    totalsize = totalsize/1000000.0
    return userfiles,totalsize

def delete_from_s3(bucketname, username,filename):
    # Upload the file
    s3_client = boto3.client('s3')

    mybucket = conn.get_bucket(bucketname)
    mybucket.delete_key(username+'/media/'+filename)
