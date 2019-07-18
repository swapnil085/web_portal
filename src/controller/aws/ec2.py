from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound

from functools import wraps
from flask import jsonify,json

#importing services
from services.aws.ec2 import Aws

aws_ec2 = Blueprint("aws_ec2",__name__,template_folder="../templates/aws/ec2")

@aws_ec2.route("/<username>/aws",methods=["GET","POST"])
def aws_dashboard(username):
    return render_template("/aws/ec2/dashboard.html",username=username)

@aws_ec2.route("/<username>/aws/ec2",methods=["GET"])
def show_instances(username):
    #all_instances = Aws.get_all_ec2_instances(username)
    return render_template("/aws/ec2/ec2_instances.html")

@aws_ec2.route("/<username>/aws/ec2/start/<instance_id>",methods=["POST"])
def start_instances(username,instance_id):

    print("start api")
    instance_dict = Aws.start(instance_id,username)
    instance_json = json.dumps(instance_dict)
    #instance_json = jsonify(instance_json)
    #print(type(instance_json))
       
    return jsonify(instance_json)

@aws_ec2.route("/<username>/aws/ec2/stop/<instance_id>",methods=["POST"])
def stop_instances(username,instance_id):
    print("stop api")
    instance_dict = Aws.stop(instance_id,username)
    instance_json = json.dumps(instance_dict)
    return instance_json
  
@aws_ec2.route("/<username>/aws/ec2/create",methods=["GET"])
def create(username):
    return render_template("/aws/ec2/test_create.html",action="created")

@aws_ec2.route("/<username>/aws/ec2/create",methods=["POST"])
def create_ec2_instance(username):
    dict = request.get_json()                                              #getting the parameters to create the instance
    instances = Aws.create_ec2_instances(username,dict)
    return

@aws_ec2.route("/<username>/aws/ec2/terminate",methods=["GET","POST"])
def terminate_ec2(username):
    print("hello")
    Aws.terminate_ec2_instance(username)
    return render_template("/aws/ec2/test_terminate.html")

@aws_ec2.route("/<username>/aws/ec2/ami",methods=["GET","POST"])
def get_aws_images(username):
    if Aws.insert_aws_images(username):
        return "inserted"
    else:
        return "error while inserting!"




