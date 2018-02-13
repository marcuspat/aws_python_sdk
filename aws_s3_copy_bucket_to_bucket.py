#!/usr/bin/env python
import sys

import boto3

# Get the service client
s3 = boto3.client('s3')

#copies an object from the source_bucket matching the keyname 
#to the destination bucket and keyname
#Don't forget to have AWSCLI setup on the machine you run this script from


copy_source = {
    'Bucket': 'source_bucket(changethis)',
    'Key': 'keyname'
}
s3.copy(copy_source, 'destination_bucket(changethis)', 'keyname')

