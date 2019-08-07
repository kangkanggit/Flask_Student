"""
负责视图，路由
"""
import hashlib
from flask import request
from flask import session
from flask import redirect
from flask import jsonify#ajax的验证
from flask import  render_template

from  FlaskDirtory.main import app
from  FlaskDirtory.models import *

#加密
def setPassword(password):
    md5 = hashlib.md5()#哈希加密
    md5.update(password.encode())#然后跟新编码
    return md5.hexdigest()#最后返回

#登录验证装饰器
def loginValid(fun):
    def inner(*args,**kwargs):
        k_user = request.cookies.get('username')
        # s_user = request.session.get('username')
        if k_user :
            user = User.quyer.filter_by(username=k_user).first()
            if user :
                return fun(*args,**kwargs)
        return redirect('/login/')
    return inner

#注册页面
@app.route('/register/',methods=["GET","POST"])
def Register():
    if request.method == "POST":#获取前端的数据
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        identity = request.form.get('identity')
        if username and password and identity:
        #保存数据
            user = User()
            user.username = username
            user.password = setPassword(password)
            user.identity = identity
            user.save()
            return redirect('/login/')
    return render_template('register.html',**locals())

#登录页面
@app.route('/login/',methods=["GET","POST"])
@loginValid
def Login():
    result ={'status':''}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                passwords = setPassword(password)
                if passwords == user.password:
                    response = redirect('/index/')
                    #设置cookie
                    response.set_cookie('username',username)
                    response.set_cookie('user_id',str(user.id))
                    return response
                else:
                    result['status']='密码不对'
            else:
                result['status']='用户名不存在'
        else:
            result['status'] = '用户密码不可以为空'
    return render_template('login.html',**locals())




#注册页面的ajax的验证
@app.route('/ajax_register/')
def ajax_register():
    result = {'status':'error','content':''}
    if request.method == 'GET':
        username = request.args.get('username')
        print(username)
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                result['content'] = '用户名存在'
            else:
                result['status'] = 'success'
                result['content'] = '用户名可以用'
        else:
            result['content'] = '用户名不可以空'
    return  jsonify(result)


#主页面
@app.route('/index/')
def index():
    return render_template('index.html',**locals())




#模板页面
@app.route('/base/')
def Base():
    return render_template('blank.html')


#退出页面
@app.route('/logout/')
def logout():
    response = redirect('/login/')
    response.delete_cookie('username')
    return response

@app.route('/student_list/')
def Student_list():
    students = Student.query.all()
    return render_template('student_list.html', **locals())