from flask import flash, session
import os
import boto3

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
    def get_all_ec2_instances(cls,username):
        session = cls.get_session(username)
        ec2 = session.resource("ec2")
        instance_list = list(ec2.instances.all())
        print(len(instance_list))
        return instance_list

    #@classmethod
    #def start_instance(cls,instance_id):


    #def Start(self):
    #    Instance = instance.start(InstanceID = [self.instanceid])
    #    #Instance = instance.start(InstanceID.N = [self.instanceid])
    #    ##https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartInstances.html
    #    return Instance

    #def Stop(self):
    #    Instance = instance.stop(InstanceID = [self.instanceid])
    #    return Instance