from flask import Blueprint, render_template, abort,request, redirect
from functools import wraps
from jinja2 import TemplateNotFound
from controller.login import *
from services.user import User

user = Blueprint("user_dashboard",__name__ , template_folder="../templates")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@user.route("/<username>/ec2",methods=["GET","POST"])
@is_logged_in
def show_ec2_instances(username):
    instance_list = User.get_all_ec2_instances(username)
    if len(instance_list)!=0:
        return render_template("ec2_instances.html",instance_list=instance_list)
    else:
        return render_template("ec2_instances.html")

@user.route("/<username>/cloudwatch",methods=["GET","POST"])
@is_logged_in
def show_cloudwatch_metrics(username):
    
