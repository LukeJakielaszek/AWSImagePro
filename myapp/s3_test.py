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
    conn = boto.connect_s3(aws_access_key_id='ASIA5NMW7G67DP5QTUFV',
                           aws_secret_access_key='/bWUZ1tK/Pj67Im9wtW8BGJxCbCC9FH9Bdhw6j5G')

    print('got connection')
    mybucket = conn.get_bucket(bucketname)
    
    print("got bucket")
    key = mybucket.new_key(filename)
    
    print('created key')
    key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
    
    print('updated bucket')
