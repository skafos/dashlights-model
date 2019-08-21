import tarfile
import boto3
from botocore.exceptions import ClientError


zip_ext = ".tar.gz"


def tarzip_file(filename):
    new_filename = filename + zip_ext
    tar = tarfile.open(new_filename, "w:gz")
    tar.add(filename)
    tar.close()
    return new_filename


# Upload & Download Functions -- make life easier -- handle zipping

def s3_upload(bucket, filename, key, tarzip=False):
    s3 = boto3.resource('s3')
    try:
        res = s3.Bucket(bucket).upload_file(Filename=filename, Key=key)
    except ClientError as e:
        print(e, flush=True)
        return False
    return True


def s3_download(bucket, filename, key, unzip=False):
    s3 = boto3.resource('s3')
    try:
        res = s3.Bucket(bucket).download_file(Filename=filename, Key=key)
        if unzip:
            with tarfile.open(filename) as tf:
                tf.extractall()
    except ClientError as e:
        print(e, flush=True)
        return False
    return True