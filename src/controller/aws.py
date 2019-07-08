from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from services.aws import Aws
from functools import wraps

aws = Blueprint("aws",__name__,template_folder="../templates/aws")

@aws.route("/<username>/aws",methods=["GET","POST"])
def aws_dashboard(username):
    return render_template("/aws/dashboard.html",username=username)

@aws.route("/<username>/aws/ec2",methods=["GET","POST"])
def ec2_instances(username):

   if request.method == "POST":
        if request.form["Start"] :
            start = request.form["Start"]
            instance_id = start.split(" ")[1]
            Aws.start(instance_id,username)

        elif request.form["Stop"]:
            stop = request.form["Stop"]
            instance_id = stop.split(" ")[1]
            Aws.stop(instance_id,username)

        elif request.form["Reboot"]:
            reboot = request.form["Reboot"]
            instance_id = reboot.split(" ")[1]
            Aws.reboot(instance_id,username)

   all_instances = Aws.get_all_ec2_instances(username)
   return render_template("/aws/ec2_instances.html",all_instances = all_instances)
  
@aws.route("/<username>/aws/ec2/create",methods=["GET","POST"])
def create_ec2(username):
    print("hello")
    instances = Aws.create_ec2_instances(username)
    return render_template("/aws/test_create.html",action="created")

@aws.route("/<username>/aws/ec2/terminate",methods=["GET","POST"])
def terminate_ec2(username):
    print("hello")
    Aws.terminate_ec2_instance(username)
    return render_template("/aws/test_terminate.html")

@aws.route("/<username>/aws/ec2/images",methods=["GET","POST"])
def get_aws_images(username):
    if Aws.insert_aws_images(username):
        return "inserted"
    else:
        return "error while inserting!"




