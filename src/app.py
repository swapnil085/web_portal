from flask import Flask, g, render_template, request ,redirect, url_for, Blueprint
from flask import flash , session
import os

# importing controllers
from controller.login import auth
from controller.user import user
from controller.aws.ec2 import aws_ec2

TEMPLATE_DIR = os.path.abspath('/templates')
app = Flask(__name__,template_folder = TEMPLATE_DIR)
app.config.from_object("config")
app.secret_key = "secret"

#importing models
from model.aws.ec2 import db
db.init_app(app)


# registering blueprints
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(aws_ec2)

@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run()
