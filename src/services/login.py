from flask import flash, session
import os
import boto3

class Login:
    @classmethod
    def login_user(self):
        username = os.getlogin()
        iam = boto3.client("iam")
        print(username)
        if iam.get_user(Username = username):
            session["logged_in"] = True
            return True
        else:
            return False
