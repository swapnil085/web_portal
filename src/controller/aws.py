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
    all_instances = Aws.get_all_ec2_instances(username)
    return render_template("/aws/ec2_instances.html",all_instances = all_instances)

@aws.route("/<username>/aws/ec2",methods=["GET","POST"])
def ec2_instances_functions(startstopinstance , username):
    all_instances = Aws.get_all_ec2_instances(username)
    Start = request.form["Start"]

    for i in all_instances:
        if Start=="Start "+str(i.id):
            InstanceID = i.id
        
    obj = Aws(InstanceID) #instanceid is passed through here
    if(Start=="Start"):
        obj.Start();
    else:
        obj.Stop();
        
    return "Working"



