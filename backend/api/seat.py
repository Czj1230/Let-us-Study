import email
import json
from flask import Blueprint, jsonify,request,render_template
from exts import db
from model import seat as seatModel
from model import merchant as merModel
from model import studyroom as roomModel
from model import record as recModel
from utils import *
from api.errors import *
seat = Blueprint('seat', __name__)

@seat.route('/list/<merchantID>',methods=['GET'])
def show_seat(merchantID):
    response_object = {}
    merchant = db.session.query(merModel).filter(merModel.id==int(merchantID)).first()
    if(merchant==None):
        return bad_request("no such merchant")
    response_object['merchantID'] = merchantID
    response_object['merchantName'] = merchant.username
    response_object['merchantShowName'] = merchant.name
    response_object['merchantPrice'] = "free"
    response_object['merchantTime'] = str(merchant.startTime)+"-"+str(merchant.endTime)
    response_object['merchantLocation'] = merchant.location
    response_object['merchantEmail'] = merchant.email
    response_object['merchantPhone'] = merchant.phone_number
    #得到商家的平均得分
    grades = merchant_average_score(merchantID)
    response_object['merchantGrade'] = round(grades,2)
    #得到商家拥挤程度
    vacancy = merchant_vacancy_score(merchantID)
    if(vacancy>0.8):
        vacancy = "crowded"
    elif(vacancy>0.4):
        vacancy = "medium"
    else:
        vacancy = "empty"
    response_object["studyroomVacancy"] = vacancy
    #得到商家所有自习室的座位情况
    response_object['StudyRoomList'] = []
    roomlist = db.session.query(roomModel).filter(roomModel.owner_id==int(merchantID))
    for rooms in roomlist:
        rseat = db.session.query(seatModel).filter(seatModel.room_id==int(rooms.id)).order_by(seatModel.specific_id.asc()).all()
        row = rooms.row
        column = rooms.column

        info = {}
        info["studyRoomID"]=rooms.id
        info["studyRoomName"]=rooms.name
        info['additional_intro'] = rooms.additional_intro
        info["seatTable"] = []
        for i in range(row):
            info["seatTable"].append([])

        for s in rseat:
            if s.status=="available":
                info["seatTable"][int((s.specific_id-1)/column)].append({"id":s.showable_id,"selected":1})
            elif s.status=="reserved":
                info["seatTable"][int((s.specific_id-1)/column)].append({"id":s.showable_id,"selected":2})
            else:
                info["seatTable"][int((s.specific_id-1)/column)].append({"id":s.showable_id,"selected":0})

        response_object['StudyRoomList'].append(info)  
    return response_object
