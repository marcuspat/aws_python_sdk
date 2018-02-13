#!/usr/bin/env python
import sys

import boto3



#this will list all buckets in your current region
#be sure to run this command from a machine where you have the awscli configured

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print bucket.name
    print "---"
    for item in bucket.objects.all():
        print "\t%s" % item.key
        
