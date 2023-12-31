from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from api.errors import error_response
from exts import db
from model import student as stuModel
from model import merchant as merModel
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
basic_auth_merchant = HTTPBasicAuth()
token_auth_merchant = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    '''用于检查用户提供的用户名和密码'''
    user = db.session.query(stuModel).filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    '''用于在认证失败的情况下返回错误响应'''
    return error_response(401)

@token_auth.verify_token
def verify_token(token):
    '''用于检查用户请求是否有token,并且token真实存在,还在有效期内'''
    g.current_user = db.session.query(stuModel).check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    '''用于在 Token Auth 认证失败的情况下返回错误响应'''
    return error_response(401)

#需要学生登陆才能使用的接口需要带上装饰器@token_auth.login_required

@basic_auth_merchant.verify_password
def verify_password(username, password):
    '''用于检查商户提供的用户名和密码'''
    user = db.session.query(merModel).filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth_merchant.error_handler
def basic_auth_error():
    '''用于在认证失败的情况下返回错误响应'''
    return error_response(401)

@token_auth_merchant.verify_token
def verify_token(token):
    '''用于检查用户请求是否有token,并且token真实存在,还在有效期内'''
    g.current_user = db.session.query(merModel).check_token(token) if token else None
    return g.current_user is not None


@token_auth_merchant.error_handler
def token_auth_error():
    '''用于在 Token Auth 认证失败的情况下返回错误响应'''
    return error_response(401)

#需要商户登陆才能使用的接口需要带上装饰器@token_auth_merchant.login_required