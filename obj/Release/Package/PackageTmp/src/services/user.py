from flask import flash, session
import os
import boto3

class User:

    @classmethod
    def get_all_ec2_instances(self,username):
        ec2 = ec2.resource("ec2")
        instance_list = ec2.instances.all()
        for instance in instance_list:
            print(instance.id, instance.state)

        return instance_list
