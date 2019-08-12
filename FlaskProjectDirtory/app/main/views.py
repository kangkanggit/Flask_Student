"""
负责视图，路由
"""
import hashlib

from flask import request
from flask import redirect
from flask import session
from flask import jsonify#ajax的验证
from flask import  render_template

from . import main
from app import csrf
from app.models import *
from .forms import *#导入表单
from app import cache#导入缓存

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
        identity = request.cookies.get('id_id')#获取身份
        # print(type(identity))
        # print(identity)
        session_username = session.get('username')#获取session
        if username and user_id and session_username :
            user = User.query.filter_by(username=username).first()
            if user and username == session_username:
                return fun(*args,**kwargs)
        return redirect('/login/')
    return inner

#注册页面
@csrf.exempt
@main.route('/register/',methods=["GET","POST"])
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

@main.route('/login/',methods=["GET","POST"])
def Login():
    result ={'status':''}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()#如果用户有下发他的身份
            # print(user)
            if user:
                identity = user.identity#获取对应的id
                # print("++++++++++++++++++++++++++++++++++++")
                # print("++++++++++++++++++++++++++++++++++++")
                passwords = setPassword(password)
                if passwords == user.password:
                    response = redirect('/index/')
                    #设置cookie
                    response.set_cookie('username',username)
                    response.set_cookie('id_id',str(identity))#下发身份必须是字符串
                    response.set_cookie('user_id',str(user.id))
                    session['username'] = username#设置seesion
                    return response
                else:
                    result['status']='密码不对'
            else:
                result['status']='用户名不存在'
        else:
            result['status'] = '用户密码不可以为空'
    return render_template('/login.html/',**locals())




#注册页面的ajax的验证
@main.route('/ajax_register/')
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
@main.route('/index/')
@loginValid
@cache.cached(timeout=500)#设置缓存
def index():
    id = request.cookies.get('user_id')
    user = User.query.get(int(id))#获取用户
    return render_template('index.html',**locals())



#老师的注册功能
@csrf.exempt
@main.route('/add_teacher/',methods=['GET','POST'])
def add_teacher():
    teacher_form = TeacherForm()
    course_list = Course.query.all()#查询所有的课程
    id = request.cookies.get('user_id')#获取用户id
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')
        id = request.form.get('id')#登录用户的id
        t = Teacher()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = course
        t.user_id = int(id)
        t.save()#保存数据
        user = User.query.get(int(id))#获取用户
        user.identity_id = 1
        user.save()#保存状态
        return redirect('/index/')
    else:
        return render_template('add_teacher.html',**locals())


#老师信息展示页面
@csrf.exempt
@main.route('/teacher_list/',methods=['GET','POST'])
def teacher_list():
    course_list = Course.query.all()  # 查询所有的课程
    teachers = Teacher.query.all()[::-1]  # 倒序，这是一个列
    return render_template('teacher_list.html', **locals())

#老师的修改功能
@csrf.exempt
@main.route('/update_teacher/',methods=['GET','POST'])
def update_teacher():
    course_list = Course.query.all()
    if request.method == 'GET':
        id = request.args.get('teacher_id')#获取老师的id
        teacher = Teacher.query.get(int(id))#获取对应的老师
        return render_template('update_teacher.html',**locals())
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        course = request.form.get('course')#获取课程
        id = request.form.get('id')#获取对应的id
        t = Teacher.query.get(int(id))
        t.name = name
        t.age = age
        t.course_id = int(course)
        t.save()
        return redirect('/teacher_list/')
#删除老师功能
@csrf.exempt
@main.route('/delete_teacher/',methods=['GET','POST'])
def delete_teacher():
    if request.method == 'GET':
        id = request.args.get('teacher_id')#获取老师id
        teacher = Teacher.query.get(int(id))
        teacher.delete_object()
        return redirect('/teacher_list')

#展示授课学生
@csrf.exempt
@main.route('/show_student/',methods=['GET','POST'])
def show_student():
    userid = request.cookies.get('user_id')#获取对应用户的id
    teacher = Teacher.query.filter_by(user_id=int(userid)).first()#获取对应的老师
    course = teacher.to_course_data#获取对应的课程
    student_list = course.to_student#获取对应的学生
#########################################查询需要优化
    return render_template('show_student.html',**locals())

#老师的个人信息页面
@csrf.exempt
@main.route('/infor_teacher/',methods=['GET','POST'])
def infor_teacher():
    id = request.cookies.get('user_id')#获取对应的用户id
    teacher = Teacher.query.filter_by(user_id=int(id)).first()#获取对应的老师
    return render_template('infor_teacher.html',**locals())

#添加学生成绩
@csrf.exempt
@main.route('/add_grade/',methods=['GET','POST'])
def grade():
    if request.method == "GET":
        user_id = request.cookies.get('user_id')#获取用户的id
        teacher = Teacher.query.filter_by(user_id=int(user_id)).first()#获取用户对应的老师
        student_id = request.args.get('student_id')#获取对应学生的id
        student = Student.query.get(int(student_id))#获取对应的学生
        courseid = teacher.to_course_data#获取对应课程的
        # print(courseid)
    else:
        pass
    return render_template('add_grade.html',**locals())

###################################学生功能区#################
#学生信息注册
@csrf.exempt
@main.route('/add_student/',methods=['GET','POST'])
def add_student():
    listcourse = []
    course_list = Course.query.all()#获取所有的课程
    if request.method == "GET":
        studentForm = StudentForm()#获取学生的注册表单
        id = request.args.get('user_id')#获取登录用户的id
        return render_template('add_student.html',**locals())
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course_list = request.form.getlist('course')#获取被选课程的id
        for course_id in course_list:
            course = Course.query.get(int(course_id))#获取对应的课程
            listcourse.append(course)
        id = request.form.get('id')#获取用户的id
        user = User.query.get(int(id))#获取对应的用户
        #先保存学生表 然后在关联用户
        student = Student()
        student.name = name
        student.age = age
        student.gender = gender
        student.user_id = int(id)
        student.to_course = listcourse
        student.save()
        user.identity_id = 1
        user.save()#表示注册完成信息
        return redirect('/index/')


#学生的个人信息表
@csrf.exempt
@main.route('/infor_student/',methods=['GET','POST'])
def infor_student():
    listcourse = []
    course_list = Course.query.all()
    if request.method == 'GET':
        id = request.cookies.get('user_id')#获取登录用户的id
        student = Student.query.filter_by(user_id = int(id)).first()
        student_course = student.to_course
        a = student_course.all()#查询课程
        return render_template('infor_student.html',**locals())
    else:
        name = request.form.get('name')
        course_id = request.form.get('course')  # 获取课程的id
        course_list = request.form.getlist('course')  # 获取被选课程的id
        for course_id in course_list:
            course = Course.query.get(int(course_id))  # 获取对应的课程
            listcourse.append(course)
        id = request.form.get('id')  # 获取用户的id
        user = User.query.get(int(id))  # 获取对应的用户
        # 先保存学生表 然后在关联用户
        student = Student.query.filter_by(name = name).first()
        student.to_course = listcourse
        student.save()
        return redirect('/infor_student/')


#学生信息展示表
@main.route('/student_list/')
def Student_list():
    students = Student.query.all()
    return render_template('student_list.html', **locals())



#学生修改功能
@csrf.exempt
@main.route('/update_student/',methods=['GET','POST'])
def update_student():
    listhh = []
    course_list = Course.query.all()
    if request.method == 'GET':
        id = request.args.get('stuid')#获取学生的id
        student = Student.query.get(int(id))
        return render_template('update_student.html',**locals())
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        id = request.form.get('id')
        courselist = request.form.getlist('course')
        for i in courselist:
            listhh.append(i)
        student = Student.query.get(int(id))#获取对应的用户
        student.name = name
        student.age = age
        student.to_course = listhh
        student.save()
        return redirect('/student_list/')

#学生的删除功
@csrf.exempt
@main.route('/delete_student/',methods=['GET','POST'])
def delete_student():
    id = request.args.get('stuid')
    stu = Student.query.get(int(id))
    stu.delete_object()
    return redirect('/student_list/')


############################课程功能区##########################
#展示课程功能
@csrf.exempt
@main.route('/list_course/',methods=['GET','POST'])
def list_course():
    course_form = CourseForm()#导入表单
    if request.method == 'GET':
        course_listed = Course.query.all()[::-1]#查询所用的课程
    else:
        label = request.form.get('label')#获取课程名
        description = request.form.get('description')#获取课程名称
        course = Course()
        course.label = label
        course.description = description
        course.save()#保存数据
        return redirect('/list_course/')
    return render_template('list_course.html',**locals())

#修改课程的功能
@csrf.exempt
@main.route('/update_course/',methods=['GET','POST'])
def update_course():
    if request.method == 'GET':
        course_id = request.args.get('course_id')#获取课程的id
        course = Course.query.get(int(course_id))#找到对应的课程
        return render_template('update_course.html',**locals())#将数据传输到修改页面
    else:
        id = request.form.get('id')
        label = request.form.get('label')
        description = request.form.get('description')
        coursed = Course.query.get(int(id))
        coursed.label = label
        coursed.description = description
        coursed.save()#保存数据
        return redirect('/list_course/')
#删除课程
@csrf.exempt
@main.route('/delete_course/',methods=['GET','POST'])
def delete_course():
    id = request.args.get('course_id')#获取前端传递的id
    course = Course.query.get(int(id))#查到对应的id
    course.delete_object()#删除课程
    return redirect('/list_course/')

###############################辅助区#############
@csrf.error_handler
@main.route("/csrf_403/")
def csrf_token_error(reason):
    print(reason) #错误信息 #The CSRF token is missing.
    return render_template("csrf_403.html",**locals())
#csrf.exempt 单视图函数避免csrf校验
#csrf.error_headler 重新定义403错误页

#模板页面
@main.route('/base/')
def Base():
    return render_template('blank.html')

#退出页面
@main.route('/logout/')
def logout():
    response = redirect('/login/')
    for i in request.cookies:
        response.delete_cookie(i)
    del session['username']
    return response

@main.route('/table/')
def Table():
    return render_template('tables.html')


#清空缓存的方法
@main.route('/clearcache/')
def clearcache():
    cache.clear()
    return 'cache 被删除'