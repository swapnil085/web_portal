from flask import flash, session
import os
import boto3
from botocore.exceptions import ClientError

#import models
from model.aws import Credential
from model.aws import Instance

class Aws():

    def __init__(self,instance_id):
        self.instance_id = instance_id

    @classmethod
    def get_session(cls,username):
        username = (username+"@sonata-software.com").lower()
        keys = Credential.get_keys_by_username(username)
        ACCESS_KEY = keys[0]
        SECRET_KEY = keys[1]
        print(keys)
        session = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name='us-east-2')
        return session
    
    @classmethod
    def get_ec2_resource(cls,username):
        session = cls.get_session(username)
        ec2 = session.resource("ec2")
        return ec2

    @classmethod
    def get_all_ec2_instances(cls,username):
        ec2 = cls.get_ec2_resource(username)
        instance_list = ec2.instances.all()
        #print(len(instance_list))
        for instance in ec2.instances.all():
            print(instance.id , instance.state)
        return instance_list

    @classmethod
    def start(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.start_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def stop(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.stop_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def reboot(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.reboot_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def create_ec2_instances(cls,username):
        ec2 = cls.get_ec2_resource(username)
        print("hello")
        instances = ec2.create_instances(ImageId="ami-00c4ae720c30116be",MinCount=1,MaxCount=1,InstanceType="t2.micro",KeyName="WinServer2012")
        Instance.add_details(username,instances[0].id)
        print(instances)
        return instances
    
    @classmethod
    def terminate_ec2_instance(cls,username):
        ec2 = cls.get_ec2_resource(username)
        #instances = ec2.terminate_instances(InstanceIds="i-02414a7407b7453ab")
        instance_id = Instance.get_id_by_username(username)
        print(instance_id)
        instances = ec2.instances.filter(InstanceIds = [instance_id]).terminate()
        print(instances)
        #return instances

    
        


    #def Start(self):
    #    Instance = EC2.instance.start(InstanceID = [self.instanceid])
    #    #Instance = instance.start(InstanceID.N = [self.instanceid])
    #    ##https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartInstances.html
    #    return Instance

    #def Stop(self):
    #    Instance = instance.stop(InstanceID = [self.instanceid])
    #    return Instance