# Let-us-Study
This platform offers you the opportunity to arrange study sessions, book study rooms, and create your personal to-do list, among other features. Feel free to explore these functionalities and give them a try!

## FrontEnd Versions

node == 16.17.1
npm == 8.15.0
vue-cli == 2.9.6

## Vue Configuration Tutorial

https://www.bilibili.com/video/BV18E411a7mC/?p=13&share_source=copy_web&vd_source=f4293d548a443af511407d90ccfd06b7

## BackEnd Versions

python == 3.6.8
flask == 2.0.3
For the rest part, please refer to requirements.txt

## Run Flask

‘cd backend’ 
‘gunicorn -c gunicorn_config.py app:app’
or 
'python3 app.py'

## Access BE interface

http://43.143.10.225:5000/

## Delete Process

ps -ef | grep gunicorn
kill -9 [pid]