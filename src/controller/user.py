from flask import Blueprint, render_template, abort,request, redirect, url_for
from functools import wraps
from jinja2 import TemplateNotFound
from controller.login import *
from services.user import User

user = Blueprint("user_dashboard",__name__ , template_folder="../templates")


