from flask import Flask
from gevent import pywsgi
import config
from exts import db
from api.merchant import *
from api.student import *
from api.tokens import tokens
from api.seat import seat
from api.studyroom import studyroom
from api.order import order
from api.todo_list import todo_list
from api.timetable import timetable
from api.countdown import countdown
# create a flask app
app = Flask(__name__)
app.config.from_object(config)
app.debug = True
# allow track and modify database
db.init_app(app)

@app.route("/")
def index():
    return "hahaha love you babe ! From Magic_Dog"

app.register_blueprint(merchant, url_prefix="/merchant")
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(tokens, url_prefix="/tokens")
app.register_blueprint(seat, url_prefix="/seat")
app.register_blueprint(studyroom, url_prefix="/studyroom")
app.register_blueprint(order, url_prefix="/order")
app.register_blueprint(todo_list, url_prefix="/todo_list")
app.register_blueprint(timetable, url_prefix="/timetable")
app.register_blueprint(countdown, url_prefix="/countdown")
if __name__ == '__main__':
    # run server
    server = pywsgi.WSGIServer(('0.0.0.0',5000),app)
    server.serve_forever()

