from flask import Flask, g, render_template, request ,redirect, url_for, Blueprint
from flask import flash , session
import os

from controller.login import user_login
from controller.user import user

TEMPLATE_DIR = os.path.abspath('/templates')
app = Flask(__name__,template_folder = TEMPLATE_DIR)
app.config.from_object("config")
app.secret_key = "secret"

# registering blueprints
# login blueprint
app.register_blueprint(user_login)
app.register_blueprint(user)

@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run()
