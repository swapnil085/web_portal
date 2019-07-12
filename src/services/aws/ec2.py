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
    def get_ec2_client(cls,username):
        username = (username+"@sonata-software.com").lower()
        keys = Credential.get_keys_by_username(username)
        ACCESS_KEY = keys[0]
        SECRET_KEY = keys[1]
        client = boto3.client("ec2",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name='us-east-2')
        return client

    @classmethod
    def get_ec2_resource(cls,username):
        session = cls.get_session(username)
        ec2 = session.resource("ec2")
        return ec2

    @classmethod
    def get_key_pair(client,key_name):
        key_pair_name = client.create_key_pair(KeyName=key_name)
        return key_pair_name

    @classmethod
    def get_all_ec2_instances(cls,username):
        ec2 = cls.get_ec2_resource(username)
        instance_list = ec2.instances.all()
        #add to instance_detail table
        for i in ec2.instances.all():
            #instance_obj = InstanceDetail(instance_id=i.id, image_id=i.image_id, instance_type=i.instance_type, zone=i.placement["AvailabilityZone"], state=i.state, key_name=i.key_name)
            ##print(i.instance_id,i.image_id)
            #InstanceDetail.add_instance_details(instance_obj)
            InstanceDetail.add_instance_details(i.instance_id,i.image_id,i.instance_type,i.placement["AvailabilityZone"],i.state["Name"],i.key_name)
        return instance_list

    @classmethod
    def start(cls,instance_id,username):
        #ec2 = cls.get_ec2_resource(username)
        #response = ec2.start_instances(InstanceIds=[instance_id],DryRun=False)
        instance = InstanceDetail.query.filter_by(instance_id=instance_id).first()
        if instance.state != "running":
            instance.state = "running"
            instance.updated_by = username
        if InstanceDetail.update_instance_detail(instance):
            return True
        else:
            return False
        print("start instance")

    @classmethod
    def stop(cls,instance_id,username):
        #ec2 = cls.get_ec2_resource(username)
        #response = ec2.stop_instances(InstanceIds=[instance_id],DryRun=False)
        instance = InstanceDetail.query.filter_by(instance_id=instance_id).first()
        if instance.state != "stopped":
            instance.state = "stopped"
            instance.updated_by = "karthik.p"
        if InstanceDetail.update_instance_detail(instance):
            return True
        else:
            return False

    @classmethod
    def reboot(cls,instance_id,username):
        ec2 = cls.get_ec2_resource(username)
        response = ec2.reboot_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def create_ec2_instances(cls,username,dict):
        ec2 = cls.get_ec2_resource(username)
        print("hello")
        #instances = ec2.create_instances(ImageId="ami-00c4ae720c30116be",MinCount=1,MaxCount=1,InstanceType="t2.micro",KeyName="WinServer2012")
        instance_id = "i-0ba1786587be36bed"
        image_id = dict["image_id"]
        instance_type = dict["instance_type"]
        zone = dict["zone"]
        state = dict["state"]
        key_name = cls.get_key_pair(client,"key"+str(datetime.now()))
        created_by = username
        updated_by = username
        InstanceDetail.add_instance_details(instance_id,image_id, instance_type, zone, state, key_name, created_by, updated_by)
        
        #return instances
    
    @classmethod
    def terminate_ec2_instance(cls,username):
        ec2 = cls.get_ec2_resource(username)
        instance_id = Instance.get_id_by_username(username)
        print(instance_id)
        instances = ec2.instances.filter(InstanceIds = ["i-01840199f504be37a"]).terminate()
        print(instances)
        #return instances
    
    @classmethod
    def insert_aws_images(cls,username):
        client = cls.get_ec2_client(username)
        images = client.describe_images(Filters=[{'Name':'platform','Values':['windows']}])
        flag = False
        for i in range(20):
            date = parse(images["Images"][i]["CreationDate"])
            if date.year >= 2016:
                image_id = images["Images"][i]["ImageId"]
                location = images['Images'][i]['ImageLocation']
                state = images['Images'][i]['State']
                public = images['Images'][i]['Public']
                name = images['Images'][i]['Name']
                architecture = images['Images'][i]['Architecture']
                platform = images['Images'][i]['Platform']
                print(architecture)
                image_obj = ImageDetail(image_id,location,public,state,name,architecture,platform)

                if ImageDetail.add_image_detail(image_obj):
                    flag = True
                else:
                    flag = False

        if flag == True:
            return True
        else:
            return False
