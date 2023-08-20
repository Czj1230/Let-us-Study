# classes of tables in database
import os
from exts import db
# import jwt
import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app

class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields

class merchant(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'merchant'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)
    name = db.Column(db.String(50))
    def __repr__(self):
        return '<Merchant {}>'.format(self.username)

    def check_password(self, password):
        '''验证密码与保存值是否匹配'''
        return self.password == password
    
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.query(merchant).filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    
    
class student(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birthdate = db.Column(db.Date)
    ranking = db.Column(db.Boolean,default = False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        '''验证密码与保存值是否匹配'''
        return self.password == password
    
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.query(student).filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    
class studyroom(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'studyroom'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    row = db.Column(db.Integer)
    column = db.Column(db.Integer)
    additional_intro = db.Column(db.String(200))
 
    
class seat(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'seat'
    universal_id = db.Column(db.Integer, primary_key=True)
    specific_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    status = db.Column(db.String(30))
    showable_id = db.Column(db.Integer)

class record(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer)
    merchant_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    seat_id = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    statu = db.Column(db.String(10))
    grade = db.Column(db.Float)
    comment = db.Column(db.Text)
    commented = db.Column(db.Boolean)
    
class merchantprofile(db.Model, EntityBase):
    #数据表名、字段
    __tablename__ = 'merchantprofile'
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer)
    location = db.Column(db.String(100))
    
class todo_list(db.Model, EntityBase):
    #数据表名、字段
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer)
    content = db.Column(db.String(200))
    checked = db.Column(db.Boolean,default = False)
    sequence = db.Column(db.Integer)

class countdown(db.Model, EntityBase):
    #数据表名、字段
    __tablename__ = 'countdown'
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer)
    content = db.Column(db.String(200))
    deadline = db.Column(db.Date)

class timetable(db.Model, EntityBase):
    #数据表名、字段
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer)
    starttime = db.Column(db.String(255))
    endtime = db.Column(db.String(255))
    content = db.Column(db.String(200))