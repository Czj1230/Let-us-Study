from flask import jsonify, g
from exts import db
from api.auth import basic_auth,token_auth,basic_auth_merchant,token_auth_merchant
from flask import Blueprint
tokens = Blueprint('tokens', __name__)


#学生端token 检索路由，以便客户端在需要 token 时调用
@tokens.route('/stu_token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    id = g.current_user.id
    db.session.commit()
    return jsonify({'token': token,'id': id})

#学生端可以向 /tokens URL发送 DELETE 请求，以使 token 失效
@tokens.route('/stu_token', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204

#商户端token 检索路由，以便客户端在需要 token 时调用
@tokens.route('/mer_token', methods=['POST'])
@basic_auth_merchant.login_required
def get_merchant_token():
    token = g.current_user.get_token()
    id = g.current_user.id
    db.session.commit()
    return jsonify({'token': token,'id': id})

#商户端可以向 /tokens URL发送 DELETE 请求，以使 token 失效
@tokens.route('/mer_token', methods=['DELETE'])
@token_auth_merchant.login_required
def revoke_merchant_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
