from flask import flash, session
import os
import boto3
from botocore.exceptions import ClientError

#import models
from model.aws import Credential

class Aws():
    @classmethod
    def get_session(cls,username):
        username = (username+"@sonata-software.com").lower()
        keys = Credential.get_keys_by_username(username)
        ACCESS_KEY = keys[0]
        SECRET_KEY = keys[1]
        print(keys)
        session = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name='us-east-1')
        return session
    
    @classmethod
    def get_ec2_resource(cls,session):
        session = cls.get_session(username)
        ec2 = session.resource("ec2")
        return ec2

    @classmethod
    def get_all_ec2_instances(cls,username):
        ec2 = cls.get_ec2_resource(username)
        instance_list = list(ec2.instances.all())
        print(len(instance_list))
        return instance_list

    @classmethod
    def start_instance(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.start_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def stop_instance(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.stop_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def create_ec2_instances(cls,image_id,key_name,min_count,max_count,instance_type):
        ec2 = cls.get_ec2_resource(username)
        instances = ec2.create_instances(ImageId=image_id,MinCount=min_count,MaxCount=max_count,InstanceType=instance_type,keyName=key_name)
        return instances


        
        


    #def Start(self):
    #    Instance = instance.start(InstanceID = [self.instanceid])
    #    #Instance = instance.start(InstanceID.N = [self.instanceid])
    #    ##https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartInstances.html
    #    return Instance

    #def Stop(self):
    #    Instance = instance.stop(InstanceID = [self.instanceid])
    #    return Instance