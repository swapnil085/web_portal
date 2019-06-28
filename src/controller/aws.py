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
    print(username)
    all_instances = Aws.get_all_ec2_instances(username)
    print(all_instances)
    return render_template("/aws/ec2_instances.html",all_instances = all_instances)

#@aws.route("/<username>/aws/ec2",methods=["post"])
#def ec2_instances_functions(startstopinstance , username):
#    all_instances = aws.get_all_ec2_instances(username)
#    start = request.form["start"]

#    for i in all_instances:
#        if start=="start "+str(i.id):
#            instanceid = i.id
        
#    obj = aws(instanceid) #instanceid is passed through here
#    if(start=="start"):
#        obj.start();
#    else:
#        obj.stop();
        
#    return redirect("/aws/<username>/ec2")



