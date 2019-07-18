from flask import flash, session
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from dateutil.parser import parse

#import models
from model.aws.ec2 import Credential
from model.aws.ec2 import Instance
from model.aws.ec2 import InstanceDetail
from model.aws.ec2 import ImageDetail

class CloudWatch():
    
    def __init__(self,instance_id,username):
        self.instance_id = instance_id
        self.username = username

    def get_cloudwatch_client(self):
        username = (self.username+"@sonata-software.com").lower()
        keys = Credential.get_keys_by_username(self.username)
        ACCESS_KEY = keys[0]
        SECRET_KEY = keys[1]
        client = boto3.client("cloudwatch",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name='us-east-2')
        return client

    def get_instance_metric(self):
        client = self.get_cloudwatch_client()
        response = client.get_metric_statistics(MetricName='DiskSpaceUtilization',Dimensions=[{'Name':'InstanceId','Value':self.instance_id}])
        return response

