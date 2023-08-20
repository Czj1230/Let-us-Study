# Here are some frequently used method

from datetime import datetime  # 有时候会返回datatime类型
from datetime import date, time
from flask_sqlalchemy import Model
from sqlalchemy import DateTime, Numeric, Date, Time  # 有时又是DateTime
from exts import db 
from model import *
 
def query_to_dict(models):
    if isinstance(models, list):
        if isinstance(models[0], Model):
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0], g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if isinstance(models, Model):
            gen = model_to_dict(models)
            dit = dict((g[0], g[1]) for g in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res
 
# 当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    # 这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res
 
def model_to_dict(model):  # 这段来自于参考资源
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)
 
def find_datetime(value):
    for v in value:
        if isinstance(value[v], datetime):
            value[v] = convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改
 
def convert_datetime(value):
    if value:
        if isinstance(value, (datetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
            return value.strftime("%H:%M:%S")
    else:
        return ""

def merchant_average_score(merchantid):
    #计算商家的平均得分
    grades = db.session.query(record).filter(record.merchant_id==merchantid,record.statu=="end",record.grade!=None).all()
    number = len(grades)
    # print("order num: "+str(number))
    total = 0.0
    for g in grades:
        total+=g.grade
    # print("total grade: "+ str(total))
    if(number==0):
        return 0.0
    else:
        return total/number

def merchant_vacancy_score(merchantid):
    active_order = db.session.query(record).filter(record.merchant_id==merchantid,record.statu.in_(["active","new"])).all()
    ordernum = len(active_order)
    # print("used seat: "+str(ordernum))
    all_seat = db.session.query(seat).join(studyroom,studyroom.id==seat.room_id).filter(studyroom.owner_id==merchantid,seat.showable_id!=0).all()
    total_seat = len(all_seat)
    # print("total seat: "+str(total_seat))
    if(total_seat==0):
        return 1.0
    else:
        return float(ordernum/total_seat)
    if(total_seat==0):
        return "crowded"
    elif(float(ordernum/total_seat)>0.8):
        return "crowded"
    elif(float(ordernum/total_seat)>0.4):
        return "medium"
    else:
        return "empty"