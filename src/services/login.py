from flask import flash, session
import os
import boto3
from ldap3 import Server, Connection

class Login():
    @classmethod
    def login_user(cls,username,password):
        server = Server('bglbg1w8dc01.sonata.local')
        conn = Connection(server,user=username,password=password)
        if conn.bind() == True:
            session["logged_in"] = True
            session["username"] = username.split("@")[0]
            return True
        else:
            return False
