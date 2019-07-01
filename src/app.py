from flask import Flask, g, render_template, request ,redirect, url_for, Blueprint
from flask import flash , session
import os

# importing controllers
from controller.login import auth
from controller.user import user
from controller.aws import aws

TEMPLATE_DIR = os.path.abspath('/templates')
app = Flask(__name__,template_folder = TEMPLATE_DIR)
app.config.from_object("config")
app.secret_key = "secret"

#importing models
from model.aws import db
db.init_app(app)


# registering blueprints
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(aws)

@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run()