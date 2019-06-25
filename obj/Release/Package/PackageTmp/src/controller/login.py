from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from services.login import Login


auth = Blueprint("user_login", __name__ , template_folder="../templates")


@auth.route("/",methods=["GET"])
@auth.route("/home",methods=["GET"])
def index():
    return render_template("index.html")

@auth.route("/login",methods=["GET","POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        if Login.login_user(username,password):
            l = username.split("@")
            name = l[0]
            return redirect(url_for(".dashboard",name=name))
        else:
            return render_template("login.html")
    return render_template("login.html")


@auth.route("/<name>",methods=["GET","POST"])
def dashboard(name):
    return render_template("dashboard.html")

@auth.route('/logout',methods=["GET","POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))
