from flask import Blueprint, render_template, abort,request, redirect, url_for,session
from jinja2 import TemplateNotFound
from services.login import Login
from functools import wraps

auth = Blueprint("user_login", __name__ , template_folder="../templates")

@auth.errorhandler(404) 
  
# inbuilt function which takes error as parameter 
def not_found(e): 
  
# defining function 
  return render_template("404.html") 

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('.login_user'))
    return wrap


@auth.route("/",methods=["GET"])
@auth.route("/home",methods=["GET"])
def index():
    if session:
        if session.get("logged_in"):
            username = session["username"]
            return redirect(url_for(".dashboard",username=username))
    return render_template("LandingPage.html")

@auth.route("/login",methods=["GET","POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if Login.login_user(username,password):
            l = username.split("@")
            name = l[0]
            return redirect(url_for(".dashboard",username=name))
        else:
            return render_template("login.html")
    else:
        if session:
            if session.get("logged_in"):
                username = session["username"]
                return redirect(url_for(".dashboard",username=username))
    return render_template("login.html")


@auth.route("/<username>",methods=["GET","POST"])
@is_logged_in
def dashboard(username):
    return render_template("dashboard.html",username=username)

@auth.route('/logout',methods=["GET","POST"])
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for(".login_user"))
