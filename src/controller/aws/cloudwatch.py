from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from functools import wraps
from flask import jsonify,json

#import services
from services.aws.ec2 import Aws
from services.aws.cloudwatch import CloudWatch

cloudwatch = Blueprint("cloudwatch",__name__,template_folder="../templates/aws/cloudwatch")

@cloudwatch.route("/<username>/aws/cloudwatch",methods=["GET"])
def get_instances(username):
    return render_template("/aws/cloudwatch/form.html")

@cloudwatch.route("/<username>/aws/cloudwatch/<instance_id>",methods=["GET"])
def show_metrics(username,instance_id):
    cwatch = CloudWatch(username,instance_id)
    d = cwatch.get_instance_metric()
    return render_template("/aws/cloudwatch/metrics.html")

