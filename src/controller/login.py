from flask import Blueprint, render_template, abort,request, redirect
from jinja2 import TemplateNotFound
from services.login import Login


user_login = Blueprint("user_login", __name__ , template_folder="../templates")


@user_login.route("/",methods=["GET"])
@user_login.route("/home",methods=["GET"])
def index():
    return render_template("index.html")


@user_login.route("/login",methods=["GET","POST"])
def login_user():
    if request.method == "GET":
        username =  Login.login_user()
        if username:
            return render_template("dashboard.html",username=username)
        else:
            return redirect(url_for("index"))
    return render_template("index.html")
