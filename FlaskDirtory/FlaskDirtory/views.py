"""
负责视图，路由
"""
import hashlib
from flask import request
from flask import redirect
from flask import jsonify#ajax的验证
from flask import  render_template

from FlaskDirtory.main import app
from FlaskDirtory.main import csrf
from FlaskDirtory.models import *
from FlaskDirtory.main import session#设置session
from FlaskDirtory.forms import TeacherForm#导入表单


#加密
def setPassword(password):
    md5 = hashlib.md5()#哈希加密
    md5.update(password.encode())#然后跟新编码
    return md5.hexdigest()#最后返回

#登录验证装饰器
def loginValid(fun):
    def inner(*args,**kwargs):
        username = request.cookies.get('username')
        user_id = request.cookies.get('user_id')
        session_username = session.get('username')#获取session
        if username and user_id and session_username:
            user = User.query.filter_by(username=username).first()
            if user :
                return fun(*args,**kwargs)
        return redirect('/login/')
    return inner

#注册页面
@csrf.exempt
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
@csrf.exempt
@app.route('/login/',methods=["GET","POST"])
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
                    session['username'] = username#设置seesion
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
        # print(username)
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
@loginValid
def index():
    return render_template('index.html',**locals())



#增加老师的页面
@csrf.exempt
@app.route('/add_teacher/',methods=['GET','POST'])
def add_teacher():

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')

        t = Teacher()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = course
        t.save()
        teacher_form = TeacherForm()
    else:
        if request.method == 'GET':
            teacher_form = TeacherForm()
    return render_template('add_teacher.html',**locals())


#老师信息展示页面
@csrf.exempt
@app.route('/teacher_list/',methods=['GET','POST'])
def teacher_list():
    teacher_form = TeacherForm()
    teachers = Teacher.query.all()[::-1]#倒序，这是一个列表
    teacher = []
    return render_template('teacher_list.html',**locals())


#删除老师功能
@csrf.exempt
@app.route('/delete_teacher/',methods=['GET','POST'])
def delete_teacher():
    if request.method == 'GET':
        id = request.args.get('teacher_id')#获取老师id
        print(id)
        teacher = Teacher.query.get(int(id))
        teacher.delete_object()
        return redirect('/teacher_list')

#修改老师信息的功能
@app.route('/update/',methods=['GET','POST'])
def update():
    teacher_form = TeacherForm()
    result = {'name':'','age':'','gender':'','course':''}
    if request.method == 'GET':
        id = request.args.get('id')
        teacher = Teacher.query.get(int(id))#获取老师
        result['name']=teacher.name
        result['age']=teacher.age
        result['gender']=teacher.gender
        result['course']=teacher.course_id
        return jsonify(result)
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')

        t = Teacher()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = course
        t.save()
    return render_template('index.html',**locals())



#学生信息增加表



#学生信息展示表
@app.route('/student_list/')
def Student_list():
    students = Student.query.all()
    return render_template('student_list.html', **locals())




@csrf.error_handler
@app.route("/csrf_403/")
def csrf_token_error(reason):
    print(reason) #错误信息 #The CSRF token is missing.
    return render_template("csrf_403.html",**locals())

#csrf.exempt 单视图函数避免csrf校验
#csrf.error_headler 重新定义403错误页

















#模板页面
@app.route('/base/')
def Base():
    return render_template('blank.html')


#退出页面
@app.route('/logout/')
def logout():
    response = redirect('/login/')
    for i in request.cookies:
        response.delete_cookie(i)
    del session['username']
    return response



@app.route('/table/')
def Table():
    return render_template('tables.html')