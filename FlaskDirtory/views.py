"""
负责视图，路由
"""
import hashlib
from flask import request
from flask import session
from flask import  render_template

from  FlaskDirtory.main import app
from  FlaskDirtory.models import *

#加密
def setPassword(password):
    md5 = hashlib.md5()#哈希加密
    md5.update(password.encode())#然后跟新编码
    return md5.hexdigest()#最后返回


@app.route('/register/',methods=["GET","POST"])
def Register():
    if request.method == "POST":#获取前端的数据
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        identity = request.form.get('identity')
        #保存数据
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identity = identity
        user.save()
    return render_template('register.html',**locals())


@app.route('/login/',methods=["GET","POST"])
def Login():
    pass

@app.route('/base/')
def Base():
    return render_template('blank.html')

@app.route('/student_list/')
def Student_list():
    students = Student.query.all()
    return render_template('student_list.html',**locals())