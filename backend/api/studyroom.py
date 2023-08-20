import email
import json
from flask import Blueprint, jsonify,request,render_template
from exts import db
from model import seat as seatModel
from model import merchant as merModel
from model import studyroom as roomModel
import ast
studyroom = Blueprint('studyroom', __name__)
    
@studyroom.route('/newroom',methods=['POST'])
def create_newroom():
    data = request.get_data()
    json_data = json.loads(data)
    merchantID=json_data['merchantID']
    studyRoomName=json_data['studyRoomName']
    seatTable = json_data['seatTable']
    intro = json_data['additional_intro']
    row = len(seatTable)
    column = len(seatTable[0])
    
    try:
        check_unique_room = db.session.query(roomModel).filter(roomModel.owner_id==merchantID, roomModel.name==studyRoomName).all()
        if(check_unique_room!=[]):
            return {"status":0}
        
        new_room = roomModel(owner_id=merchantID, name=studyRoomName, row=row, column=column, additional_intro=intro)
        db.session.add(new_room)
        db.session.commit()
        room = db.session.query(roomModel).filter(roomModel.owner_id==merchantID, roomModel.name==studyRoomName).first()
        rid = room.id
        sid = 1
        for r in range(row):
            for c in range(column):
                if(seatTable[r][c]==0):
                    new_seat = seatModel(specific_id = sid, room_id = rid, status = "unavailable", showable_id = seatTable[r][c])
                else:
                    new_seat = seatModel(specific_id = sid, room_id = rid, status = "available", showable_id = seatTable[r][c])
                db.session.add(new_seat)
                sid+=1
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}
    
@studyroom.route('/<roomID>',methods=['DELETE'])
def delete_room(roomID):
    try:
        check_unique_room = db.session.query(roomModel).filter(roomModel.id==roomID).first()
        if check_unique_room is None:
            return {"status":0}
        db.session.execute('SET FOREIGN_KEY_CHECKS=0;')
        db.session.query(roomModel).filter(roomModel.id==roomID).delete()
        db.session.execute('SET FOREIGN_KEY_CHECKS=1;')
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@studyroom.route('/<roomID>',methods=['PUT'])
def edit_room(roomID):
    name = request.args.get('name')
    seatTable = ast.literal_eval(request.args.get('seatTable')) if request.args.get('seatTable') is not None else None
    additional_intro = request.args.get('additional_intro')
    room = db.session.query(roomModel).filter(roomModel.id==roomID).first()
    try:
        if room is None:
            return {"status":0}
        if name is not None:
            room.name = name
        if seatTable is not None:
            row = len(seatTable)
            column = len(seatTable[0])
            db.session.query(seatModel).filter(seatModel.room_id==roomID).delete()
            room.row = row
            room.column = column
            sid = 1
            for r in range(row):
                for c in range(column):
                    if(seatTable[r][c]==0):
                        new_seat = seatModel(specific_id = sid, room_id = roomID, status = "unavailable", showable_id = seatTable[r][c])
                    else:
                        new_seat = seatModel(specific_id = sid, room_id = roomID, status = "available", showable_id = seatTable[r][c])
                    db.session.add(new_seat)
                    sid+=1
        if additional_intro is not None:
            room.additional_intro = additional_intro
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
        