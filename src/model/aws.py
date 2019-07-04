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
    instance_id = db.Column(db.String(255), nullable=False,unique=True)
    instance_detail = db.relationship("InstanceDetail",backref="instance_detail")

    def __init__(self,username,instance_id):
        self.username = username
        self.instance_id = instance_id


    @classmethod
    def get_id_by_username(cls,username):
        instance = Instance.query.filter_by(username=username).first()
        instanceId = instance.instance_id
        return instanceId
    
    @classmethod
    def get_username_by_instanceId(cls,instanceId):
       uname = Instance.query.filter_by(instance_id=instanceId).first()
       return uname

    @classmethod
    def add_details(cls,username,instance_id):
       instance_obj = Instance(username=username,instance_id=instance_id)
       try:
           db.session.add(instance_obj)
           db.session.commit()
       except:
           db.session.rollback()

class InstanceDetail(db.Model):
    __tablename__ = "instance_detail"
    details_id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.Integer,db.ForeignKey("instance.iid"))
    image_id = db.Column(db.String(255),nullable=False)
    instance_type = db.Column(db.String(255),nullable=False)
    region = db.Column(db.Enum("us-east-1","us-east-2","us-west-1","us-west-2","ap-south-1","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1","eu-central-1","eu-west-1","sa-east-1"))
    state = db.Column(db.Enum("pending","running","shutting-down","terminated","stopping","stopped","rebooting"))
    instance = db.relationship("Instance",backref="instance")

    def __init__(self,instance_id,image_id,instance_type,region,state):
        self.instance_id = instance_id
        self.image_id = image_id
        self.instance_type = instance_type
        self.region = region
        self.state = state

    @classmethod
    def add_instance_details(cls,obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except:
            db.session.rollback()
    
    @classmethod
    def delete_instance_details(cls,obj):
        try:
            db.session.delete(obj)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def instane_by_region(cls,zone):
        try:
            instance_list = InstanceDetail.query.filter(region=zone).all()
            return instance_list
        except:
            return False


    


