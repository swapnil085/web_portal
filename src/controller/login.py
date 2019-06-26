from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from services.login import Login
from functools import wraps

auth = Blueprint("user_login", __name__ , template_folder="../templates")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_user'))
    return wrap


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
            username = name
            return redirect(url_for(".dashboard",username=username))
        else:
            return render_template("login.html")
    return render_template("login.html")


@auth.route("/<username>",methods=["GET","POST"])
@is_logged_in
def dashboard(username):
    return render_template("dashboard.html",username=username)

@auth.route('/logout',methods=["GET","POST"])
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for("index"))
