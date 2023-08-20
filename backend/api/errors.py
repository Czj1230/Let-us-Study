from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from api.merchant import merchant
from api.student import student
from exts import db


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    response.headers["WWW-Authenticate"] = None
    return response


def bad_request(message):
    '''最常用的错误 400:错误的请求'''
    return error_response(400, message)


@merchant.app_errorhandler(404)
@student.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@merchant.app_errorhandler(500)
@student.app_errorhandler(404)
def internal_error(error):
    db.session.rollback()
    return error_response(500)