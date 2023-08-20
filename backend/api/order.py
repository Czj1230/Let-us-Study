import email
import json
import time
from flask import Blueprint, jsonify,request,render_template
from exts import db
from model import seat as seatModel
from model import merchant as merModel
from model import studyroom as roomModel
from model import record as recModel
from model import student as stuModel
import sqlalchemy as sa
order = Blueprint('order', __name__)

#新建订单
@order.route('/create',methods=['POST'])
def new_order():
    data = request.get_data()
    json_data = json.loads(data)
    studentID=json_data['studentID']
    merchantID=json_data['merchantID']
    studyRoomID=json_data['studyRoomID']
    seatID=json_data['seatName']            # 注意！！！创建订单提交的是showable_id
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    new_order = recModel(stu_id = studentID, merchant_id = merchantID, room_id = studyRoomID, seat_id = seatID, starttime = now, statu = "new")
    # 添加flask-sqlalchemy 行锁 .with_for_update()
    seat_to_reserve = db.session.query(seatModel).filter(seatModel.room_id==studyRoomID,seatModel.showable_id==seatID).with_for_update(read=False).first()
    try: #1.加入新订单 2.修改座位状态为“已预订”
        if seat_to_reserve.status !="reserved":
            db.session.add(new_order)
            seat_to_reserve.status="reserved"
            db.session.commit()
            return {"status":1,"timestamp":now}
    except Exception as e:
        return {"status":0,"timestamp":now}
        
#定时器：为new状态的订单，30min后没有修改状态则从new-->scrap
#触发器：若订单从new-->scrap，相应座位从reserved-->available

@order.route('/listForMerchant/<merchantID>',methods=['GET'])
def list_merchant_order(merchantID):
    response_object = {}
    merchant = db.session.query(merModel).filter(merModel.id==merchantID).first()
    if(merchant==None):
        return {"merchantName":None,"merchantLocation":None,"records":[]}
    response_object['merchantName']=merchant.username
    response_object['merchantShowName']=merchant.name
    response_object['merchantLocation']=merchant.location if merchant.location!=None else ""
    response_object['records']=[]
    all_records = db.session.query(recModel).filter(recModel.merchant_id==merchantID).all()
    for r in all_records:
        ans = {}
        ans['recordId']=r.id
        room = db.session.query(roomModel).filter(roomModel.id==r.room_id).first()
        ans['studentId']=r.stu_id
        ans['roomName']=room.name if room!=None else ""
        ans['seatId']=r.seat_id
        ans['startTime']=r.starttime.strftime("%Y-%m-%d %H:%M:%S")
        ans['endTime']=r.endtime.strftime("%Y-%m-%d %H:%M:%S") if r.endtime!=None else ""
        ans['state']=r.statu
        response_object['records'].append(ans)
    
    return response_object

@order.route('/listForStudent/<studentID>',methods=['GET'])
def list_student_order(studentID):
    response_object = {}
    student = db.session.query(stuModel).filter(stuModel.id==studentID).first()
    if(student==None): #if the student id is not valid, then return empty object
        return {"records":[]}
    
    response_object['records']=[]
    all_records = db.session.query(recModel).filter(recModel.stu_id==studentID).all()
    for r in all_records:
        ans = {}
        ans['recordId']=r.id
        merchant = db.session.query(merModel).filter(merModel.id==r.merchant_id).first()
        ans['merchantName']=merchant.username
        ans['merchantShowName']=merchant.name
        ans['merchantLocation']=merchant.location if merchant.location!=None else ""
        room = db.session.query(roomModel).filter(roomModel.id==r.room_id).first()
        ans['roomName']=room.name if room!=None else "(None)"
        ans['seatId']=r.seat_id
        ans['startTime']=r.starttime.strftime("%Y-%m-%d %H:%M:%S")
        ans['endTime']=r.endtime.strftime("%Y-%m-%d %H:%M:%S") if r.endtime!=None else ""
        ans['state']=r.statu
        ans['commented']=r.commented
        response_object['records'].append(ans)
    
    return response_object

@order.route('/comment',methods=['POST'])
def submit_comment():
    data = request.get_data()
    json_data = json.loads(data)
    recordId=json_data['recordId']
    comment = json_data['comment']
    facility = float(json_data['facility']) if json_data['facility']!=None else 0
    confortLevel = float(json_data['confortLevel']) if json_data['confortLevel']!=None else 0
    quietness = float(json_data['quietness']) if json_data['quietness']!=None else 0
    average_grade = (facility+confortLevel+quietness)/3
    record = db.session.query(recModel).filter(recModel.id==recordId).first()
    try: #
        if comment!="":
            record.comment = comment
            record.commented = 1    #标记已评论
        if average_grade!=0:
            record.grade = average_grade
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}

@order.route('/comment/<merchantID>',methods=['GET'])
def list_merchant_comment(merchantID):
    response_object = {}
    merchant = db.session.query(merModel).filter(merModel.id==merchantID).first()
    if(merchant==None): #if the student id is not valid, then return empty object
        return {"records":[]}
    
    response_object['records']=[]
    all_records = db.session.query(recModel).filter(recModel.merchant_id==merchantID,recModel.comment !=sa.null()).order_by(recModel.id.desc()).all()
    for r in all_records:
        ans = {}
        ans['recordId']=r.id
        ans['comment']=r.comment
        ans['endTime']=r.endtime.strftime("%Y-%m-%d %H:%M:%S") if r.endtime!=None else ""
        ans['state']=r.statu
        ans['grade'] = round(r.grade,2) if r.grade != None else 0
        response_object['records'].append(ans)
    
    return response_object

@order.route('/signIn',methods=['POST'])
def sign_in_and_out():
    data = request.get_data()
    json_data = json.loads(data)
    recordId=json_data['recordId']
    state = json_data['state']
    record = db.session.query(recModel).filter(recModel.id==recordId).first()
    seat = db.session.query(seatModel).filter(seatModel.room_id==record.room_id,seatModel.showable_id==record.seat_id).first()
    try: #
        if(state=="active"):#试图签到
            if(record.statu!="new" or seat.status!="reserved"): #只有当前状态为new的订单且座位为已预订才可以签到
                return {"status":0}
            record.statu = state #修改订单状态

        elif(state=="end"):#试图签离
            if(record.statu!="active" or seat.status!="reserved"): #只有当前状态为active的订单且座位为已预订才可以签离
                return {"status":0}
            record.statu = state
            seat.status = "available"  #释放座位
            record.endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) #订单更新签离时间
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}