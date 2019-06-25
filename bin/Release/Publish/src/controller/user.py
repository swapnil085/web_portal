from flask import Blueprint, render_template, abort,request, redirect, url_for
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
