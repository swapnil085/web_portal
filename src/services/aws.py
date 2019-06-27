from flask import flash, session
import os
import boto3

class Aws():
    def __init__(self, Instanceid):
            self.instanceid = Instanceid

    @classmethod
    def get_session(self,username):
        # get access_key and secret_key from database based on the username
        session = boto3.session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        return session

    @classmethod
    def get_all_ec2_instances(self,username):
        session = self.get_session(username)
        ec2 = session.resource("ec2")
        instance_list = ec2.instances.all()
        return instance_list

    def Start(self):
            Instance = instance.start(InstanceID = [self.instanceid])
            #Instance = instance.start(InstanceID.N = [self.instanceid])
            ##https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_StartInstances.html
            return Instance

    def Stop(self):
            Instance = instance.stop(InstanceID = [self.instanceid])
            return Instance