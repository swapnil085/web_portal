from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from services.aws import Aws
from functools import wraps

aws = Blueprint("aws",__name__,template_folder="../templates/aws")

@aws.route("/<username>/aws",methods=["GET","POST"])
def aws_dashboard(username):
    return render_template("/aws/dashboard.html",username=username)

@aws.route("/<username>/aws/ec2",methods=["GET"])
def show_instances(username):
    #all_instances = Aws.get_all_ec2_instances(username)
    return render_template("/aws/ec2_instances.html")

@aws.route("/<username>/aws/ec2/start/<instance_id>",methods=["POST"])
def start_instances(username,instance_id):

    print("start api")
    if Aws.start(instance_id,username):
        return "started"
    else:
        return "error starting"

@aws.route("/<username>/aws/ec2/stop/<instance_id>",methods=["POST"])
def stop_instances(username,instance_id):

    print("stop api")
    if Aws.stop(instance_id,username):
        return "stopped"
    else:
        return "error stopping"
  
@aws.route("/<username>/aws/ec2/create",methods=["GET"])
def create(username):
    return render_template("/aws/test_create.html",action="created")

@aws.route("/<username>/aws/ec2/create",methods=["POST"])
def create_ec2_instance(username):
    dict = request.get_json()                                                   #getting the parameters to create the instance
    instances = Aws.create_ec2_instances(username,dict)
    return

@aws.route("/<username>/aws/ec2/terminate",methods=["GET","POST"])
def terminate_ec2(username):
    print("hello")
    Aws.terminate_ec2_instance(username)
    return render_template("/aws/test_terminate.html")

@aws.route("/<username>/aws/ec2/ami",methods=["GET","POST"])
def get_aws_images(username):
    if Aws.insert_aws_images(username):
        return "inserted"
    else:
        return "error while inserting!"




