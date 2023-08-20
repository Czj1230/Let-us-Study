import email
import json
from flask import Blueprint, jsonify,request,render_template
from exts import db
from datetime import datetime
from model import student as stuModel
from model import record as recModel
student = Blueprint('student', __name__)

@student.route('/insert',methods=['POST'])
def insert_student():
    data = request.get_data()
    json_data = json.loads(data)
    username=json_data['username']
    password = json_data['password']
    gender = json_data['gender']
    email = json_data['email'] if "email" in json_data else ""
    birthday = datetime.strptime(json_data['birthday'],'%Y-%m-%d') if "birthday" in json_data else None
    try:
        if db.session.query(stuModel).filter(stuModel.username==username).first() is not None:
            return {"status":0,"message":'student username has already existed'}
        user = stuModel(username = username,password = password,gender = gender,email = email,birthdate = birthday)
        db.session.add(user)   
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}
    
@student.route('/getRanking',methods=['GET'])
def GetRangkingInfo():
    response_object = {}
    students = db.session.query(stuModel)
    if(students == None):
        return {"rankinglist":[]}
    response_object['rankinglist']=[]
    for student in students:
        ans = {}
        ans['name'] = student.username
        records = db.session.query(recModel).filter(recModel.stu_id == student.id, recModel.statu == "end").all()
        score = len(records)
        ans['score'] = score
        response_object['rankinglist'].append(ans)
    
    return response_object