from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as encrpyt
import datetime

db = SQLAlchemy()

class Credential(db.Model):
    __tablename__ = "credential"
    cid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),nullable=False)
    access_key = db.Column(db.String(255),nullable=False)
    secret_key = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now())
    created_by = db.Column(db.String(255),nullable=False)

    def __init__(self,username,access_key,secret_key,created_at,created_by):
        self.username = username
        self.access_key = access_key
        self.secret_key = secret_key
        self.created_at = created_at
        self.created_by = created_by

    @classmethod
    def get_keys_by_username(cls,username):
        cred_obj = Credential.query.filter_by(username=username).first()
        keys = [cred_obj.access_key, cred_obj.secret_key]
        return keys

class Instance(db.Model):
    __tablename__ = "instance"
    iid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    instance_id = db.Column(db.String(255), nullable=False)

    def __init__(self,username,instance_id):
        self.username = username
        self.instance_id = instance_id


    @classmethod
    def get_id_by_username(cls,username):
        instanceId = Instance.query.filter_by(username=username).first()
        return instanceId
    
    @classmethod
    def get_username_by_instanceId(cls,instanceId):
       uname = Instance.query.filter_by(instance_id=instanceId).first()
       return uname