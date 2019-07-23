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
    #instance_detail = db.relationship("InstanceDetail",backref="instance_detail")

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
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(255),nullable=False)
    image_id = db.Column(db.String(255),nullable=False)
    instance_type = db.Column(db.String(255),nullable=False)
    zone = db.Column(db.String(255),nullable=False)
    state = db.Column(db.Enum("pending","running","shutting-down","terminated","stopping","stopped","rebooting"))
    key_name = db.Column(db.String(255),nullable=False,default="WinServer2012")
    created_by = db.Column(db.String(255),nullable=False)
    updated_by = db.Column(db.String(255),nullable=False)

    def __init__(self,instance_id,image_id,instance_type,zone,state,key_name,created_by,updated_by):
        self.instance_id = instance_id
        self.image_id = image_id
        self.instance_type = instance_type
        self.zone = zone
        self.state = state
        self.key_name = key_name
        self.created_by = created_by
        self.updated_by = updated_by

    @classmethod
    def class_to_dict(cls,obj):
        d=dict()
        d = {
                "instance_id":obj.instance_id,
                "image_id":obj.image_id,
                "instance_type":obj.instance_type,
                "zone":obj.zone,
                "state":obj.state,
                "key_name":obj.key_name,\
                "created_by":obj.created_by,
                "updated_by":obj.updated_by
            }
        return d

    @classmethod
    def add_instance_details(cls,instance_id,image_id,instance_type,zone,state,key_name,created_by,updated_by):
        obj = InstanceDetail(instance_id=instance_id, image_id=image_id, instance_type=instance_type, zone=zone, state=state, key_name=key_name, created_by=created_by, updated_by=updated_by)
        try:
            print("1")
            db.session.add(obj)
            db.session.commit()
        except:
            print("2")
            db.session.rollback()
        return

    @classmethod
    def delete_instance_details(cls,instance_id,image_id,instance_type,zone,state,key_name):
        obj = InstanceDetail(instance_id=instance_id, image_id=image_id, instance_type=instance_type, zone=zone, state=state, key_name=key_name)
        try:
            db.session.delete(obj)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def instance_by_zone(cls,zone):
        try:
            instance_list = InstanceDetail.query.filter(zone=zone).all()
            return instance_list
        except:
            return False

    @classmethod
    def update_instance_detail(cls,instance):
        try:
            db.session.commit()
            d = InstanceDetail.class_to_dict(instance)
            print(d)
            return d
        except:
            db.session.rollback()
            return False

class ImageDetail(db.Model):
    __tablename__ = "image_detail"
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(255),nullable=False)
    location = db.Column(db.String(255),nullable=False)
    public = db.Column(db.Boolean, nullable = False, default = True)
    state = db.Column(db.Enum('pending','available','invalid','deregistered','transient','failed','error'),default='available')
    name = db.Column(db.String(255))
    architecture = db.Column(db.String(255),nullable=False)
    platform = db.Column(db.String(255),nullable=False)

    def __init__(self, image_id, location, public, state, name, architecture,platform):
        self.image_id = image_id
        self.location = location
        self.public = public 
        self.state = state
        self.name = name
        self.architecture = architecture
        self.platform = platform

    @classmethod
    def add_image_detail(cls,image_obj):
        try:
            db.session.add(image_obj)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @classmethod
    def get_image_by_location(cls,location):
        try:
            images = ImageDetail.query.filter(location=location).all()
            return images
        except:
            return []