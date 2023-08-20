import json
from flask import Blueprint,request
from exts import db
from model import todo_list as todoModel
todo_list = Blueprint('todo_list', __name__)
def str_to_bool(str):
    return True if str.lower() == 'true' else False
@todo_list.route('/create',methods=['POST'])
def new_todo():
    data = request.get_data()
    json_data = json.loads(data)
    studentID=json_data['studentID']
    content=json_data['content']
    checked=json_data['checked']
    #checked bool 1是0否
    sequence=json_data['sequence']
    #sequence int紧急程度：分为两种，1重要 0普通，前端可以给两个选项
    new_todo = todoModel(stu_id = studentID, content = content, checked=checked,sequence=sequence)
    try: 
        db.session.add(new_todo)
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@todo_list.route('/list/<studentID>',methods=['GET'])
def list_todo(studentID):
    response_object = {}
    response_object['all_todos'] = []
    todos = db.session.query(todoModel).filter(todoModel.stu_id==studentID).order_by(todoModel.sequence.desc()).all()
    for m in todos:
        ans = {}
        ans['id']=m.id
        ans['content']=m.content
        ans['checked']=m.checked
        ans['sequence']=m.sequence
        response_object['all_todos'].append(ans)
    return response_object

@todo_list.route('/<todoID>',methods=['PUT'])
def edit_todo(todoID):
    content = request.args.get('content')
    checked = request.args.get('checked')
    sequence = request.args.get('sequence')
    todo = db.session.query(todoModel).filter(todoModel.id==todoID).first()
    try:
        if todo is None:
            return {"status":0}
        if content is not None:
            todo.content = content
        if checked is not None:
            todo.checked = str_to_bool(checked)
        if sequence is not None:
            todo.sequence = sequence
        db.session.commit()
        return {"status":1}
    except Exception as e:
        print(e)
        return {"status":0}
    
@todo_list.route('/<todoID>',methods=['DELETE'])
def delete_todo(todoID):
    try:
        check_unique_todo = db.session.query(todoModel).filter(todoModel.id==todoID).first()
        if check_unique_todo is None:
            return {"status":0}
        db.session.query(todoModel).filter(todoModel.id==todoID).delete()
        db.session.commit()
        return {"status":1}
    except Exception as e:
        return {"status":0}