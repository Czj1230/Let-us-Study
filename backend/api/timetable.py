import json
from flask import Blueprint,request
from exts import db
from model import timetable as timeModel
from sqlalchemy import and_
import time
timetable = Blueprint('timetable', __name__)


@timetable.route('/create',methods=['POST'])
def new_timetable():
    data = request.get_data()
    json_data = json.loads(data)
    studentID=json_data['studentID']
    content=json_data['content']
    starttime = json_data['starttime'] 
    endtime = json_data['endtime'] 
    new_timetable = timeModel(stu_id = studentID, content = content,starttime=starttime,endtime = endtime)
    try: 
        db.session.add(new_timetable)
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@timetable.route('/list/<studentID>',methods=['GET'])
def list_timetable(studentID):
    response_object = {}
    response_object['all_timetables'] = []
    timetables = db.session.query(timeModel).filter(timeModel.stu_id==studentID).order_by(timeModel.starttime.desc()).all()
    for m in timetables:
        ans = {}
        ans['id']=m.id
        ans['content']=m.content
        ans['starttime']=m.starttime
        ans['endtime']=m.endtime
        response_object['all_timetables'].append(ans)
    return response_object

@timetable.route('/<timetableID>',methods=['PUT'])
def edit_timetable(timetableID):
    content = request.args.get('content')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    timetable = db.session.query(timeModel).filter(timeModel.id==timetableID).first()
    try:
        if timetable is None:
            return {"status":0}
        if content is not None:
            timetable.content = content
        if starttime is not None:
            timetable.starttime = starttime
        if endtime is not None:
            timetable.endtime = endtime 
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@timetable.route('/<timetableID>',methods=['DELETE'])
def delete_timetable(timetableID):
    try:
        check_unique_timetable = db.session.query(timeModel).filter(timeModel.id==timetableID).first()
        if check_unique_timetable is None:
            return {"status":0}
        db.session.query(timeModel).filter(timeModel.id==timetableID).delete()
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}