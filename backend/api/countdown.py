import json
from flask import Blueprint,request
from exts import db
from model import countdown as countModel
from sqlalchemy import and_
from datetime import datetime
countdown = Blueprint('countdown', __name__)

@countdown.route('/create',methods=['POST'])
def new_countdown():
    data = request.get_data()
    json_data = json.loads(data)
    studentID=json_data['studentID']
    content=json_data['content']
    deadline = datetime.strptime(json_data['deadline'], '%Y-%m-%d') if "deadline" in json_data else None
    new_countdown = countModel(stu_id = studentID, content = content,deadline=deadline)
    try: 
        db.session.add(new_countdown)
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@countdown.route('/list/<studentID>',methods=['GET'])
def list_countdown(studentID):
    response_object = {}
    response_object['all_countdowns'] = []
    countdowns = db.session.query(countModel).filter(countModel.stu_id==studentID).all()
    for m in countdowns:
        ans = {}
        ans['id']=m.id
        ans['content']=m.content
        ans['deadline']=m.deadline
        response_object['all_countdowns'].append(ans)
    return response_object

@countdown.route('/<countdownID>',methods=['PUT'])
def edit_countdown(countdownID):
    content = request.args.get('content')
    deadline = datetime.strptime(request.args.get('deadline'), '%Y-%m-%d') if request.args.get('deadline') is not None else None
    countdown = db.session.query(countModel).filter(countModel.id==countdownID).first()
    try:
        if countdown is None:
            return {"status":0}
        if content is not None:
            countdown.content = content
        if deadline is not None:
            countdown.deadline = deadline
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@countdown.route('/<countdownID>',methods=['DELETE'])
def delete_countdown(countdownID):
    try:
        check_unique_countdown = db.session.query(countModel).filter(countModel.id==countdownID).first()
        if check_unique_countdown is None:
            return {"status":0}
        db.session.query(countModel).filter(countModel.id==countdownID).delete()
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}