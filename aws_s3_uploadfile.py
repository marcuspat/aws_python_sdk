#!/usr/bin/env python

import boto3

# Get the service client
s3 = boto3.client('s3')

#take the file you specify and uploads it to the bucket with the object name.


s3.upload_file("file to upload", "bucketname", "objectname")

