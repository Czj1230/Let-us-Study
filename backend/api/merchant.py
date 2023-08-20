import email
import json
import os
from flask import Blueprint, jsonify,request,render_template,make_response
from exts import db
from model import merchant as merModel
from model import merchantprofile as profileModel
from model import record as recModel
from model import studyroom as roomModel
from model import seat as seatModel
from utils import *
import time

merchant = Blueprint('merchant', __name__)

@merchant.route('/list')
def list_merchant():
    response_object = {}
    response_object['all_merchant'] = []
    merchants = db.session.query(merModel).all()
    for m in merchants:
        ans = {}
        ans['merchantId']=m.id
        ans['merchantName']=m.username
        ans['merchantShowName']=m.name if m.name!=None else ""
        ans['merchantLocation']=m.location if m.location!=None else ""
        #得到商家的图片路径
        img = db.session.query(profileModel).filter(profileModel.merchant_id==m.id).first()
        ans['merchantImage']=img.location if img!=None else ""
        #得到商家的平均得分
        ave_grade = merchant_average_score(m.id)
        ans['merchantGrade'] = round(ave_grade,2)
        #得到拥挤程度
        vacancy = merchant_vacancy_score(m.id)
        ans["studyroomVacancy"]=vacancy

        response_object['all_merchant'].append(ans)
        
    return response_object

@merchant.route('/insert',methods=['POST'])
def insert_merchant():
    data = request.get_data()
    json_data = json.loads(data)
    username=json_data['username']
    name = json_data['name'] if "name" in json_data else ""
    password = json_data['password']
    email = json_data['email'] if "email" in json_data else ""
    phone_number = json_data['phone_number']  if "phone_number" in json_data else ""
    try:
        if db.session.query(merModel).filter(merModel.username==username).first() is not None:
            return {"status":0,"message":'merchant username has already existed'}
        db.session.execute(
            "insert into merchant (username, name, password, email, phone_number) values"\
            "(\""+username+"\",\""+name+"\",\""+password+"\",\""+email+"\",\""+phone_number+"\")"
        )
        db.session.commit()
        return {"status":1}
    # username & password在数据库中设置为not null，故而若为空，则插入会失败
    except Exception as e:
        return {"status":0}

#设置商家信息
@merchant.route('/setting/<merchantId>',methods=['POST'])
def set_merchant(merchantId):
    data = request.get_data()
    json_data = json.loads(data)
    merchantname=json_data['merchantName'] if json_data['merchantName']!=None else ""
    merchantshowname=json_data['merchantShowName'] if json_data['merchantShowName']!=None else ""
    location = json_data['merchantLocation'] if json_data['merchantLocation']!=None else ""
    # stime = json_data['merchantStartTime']
    stime = time.strptime(json_data['merchantStartTime'],'%H:%M:%S') if json_data['merchantStartTime']!=None else ""
    # etime = json_data['merchantEndTime']
    etime = time.strptime(json_data['merchantEndTime'],'%H:%M:%S') if json_data['merchantEndTime']!=None else ""
    try:
        m = db.session.query(merModel).filter(merModel.id==merchantId).first()
        m.username = merchantname if merchantname!="" else m.username #不为空的项才会修改
        m.name = merchantshowname if merchantshowname!="" else m.name
        m.location = location if location!="" else m.location
        m.startTime = stime if stime!="" else m.startTime
        m.endTime = etime if etime!="" else m.endTime
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}

@merchant.route('/uploadImg',methods=['POST'])
def save_uploadImg():
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 通过表单中name值获取图片
    imgData = request.files["image"]
    merchantId = request.form.get("merchantId")
    # 设置图片要保存到的路径
    path = basedir + "/image/"
    # print(path)
    # 获取图片名称及后缀名
    imgName = imgData.filename

    # 图片path和名称组成图片的保存路径
    file_path = path + imgName

    # 保存图片
    try:
        imgData.save(file_path)
        merchant = db.session.query(profileModel).filter(profileModel.merchant_id==merchantId).first()
        if(merchant==None): #商家第一次上传图片，表中添加新的条目
            newProfile = profileModel(merchant_id=merchantId,location=file_path)
            db.session.add(newProfile)
        else: #商家更新图片，修改该商家的条目信息
            merchant.location = file_path
        db.session.commit()

        # url是图片的路径
        url = file_path
        return {"imageUrl":url}
    except Exception:
        return {"imageUrl":"fail"}

@merchant.route('/getImg/<merchantId>',methods=['GET'])
# def get_Image(merchantId):
#     img = db.session.query(profileModel).filter(profileModel.merchant_id==merchantId).first()
#     file_name = img.location.split('/')[-1]
#     print(file_name)
#     picture_data = {
#         "file_name": file_name,
#         "url": "http://127.0.0.1:5000/backend/api/image/"+file_name
#     }
#     return jsonify(picture_data)
def get_Image(merchantId):
    basedir = os.path.abspath(os.path.dirname(__file__))
    img = db.session.query(profileModel).filter(profileModel.merchant_id==merchantId).first()
    if img!=None:
        file_name = img.location.split('/')[-1]
    else: #没有上传过图片的商家，后端返回默认图片
        file_name = "test.png"
    path = basedir + "/image/"+file_name
    image_data = open(path, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png' #返回的内容类型必须修改
    
    return response

@merchant.route('/<merchantID>',methods=['PUT'])
def edit_merchant(merchantID):
    name = request.args.get('merchantName')
    show_name = request.args.get('merchantShowName')
    location = request.args.get('merchantLocation')
    stime = time.strptime(request.args.get('merchantStartTime'),'%H:%M:%S') if request.args.get('merchantStartTime')!=None else None
    etime = time.strptime(request.args.get('merchantEndTime'),'%H:%M:%S') if request.args.get('merchantEndTime')!=None else None
    merchant = db.session.query(merModel).filter(merModel.id==merchantID).first()
    try:
        if merchant is None:
            return {"status":0}
        if name is not None:
            check_unique_name = db.session.query(merModel).filter(merModel.username==name).first()
            if check_unique_name is not None:
                return {"status":0}
            merchant.username = name
        if show_name is not None:
            merchant.name = show_name
        if location is not None:
            merchant.location = location
        if stime is not None:
            merchant.startTime = stime
        if etime is not None:
            merchant.endTime = etime
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}