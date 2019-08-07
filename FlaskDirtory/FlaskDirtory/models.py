"""
搭建数据库模型
"""
from FlaskDirtory.main import models

session = models.session
class BaseNodel(models.Model):
    __abstract__ = True#代表当前类是抽象的，不会被创建
    id = models.Column(models.Integer,primary_key=True,autoincrement=True)
    #保存数据的方法
    def save(self):
        session.add(self)
        session.commit()#固定用法
    def delete_object(self):
        session.delete(self)
        session.commit()

#用户中心
class User(BaseNodel):
    __tablename__ = 'user'
    username = models.Column(models.String(32))
    password = models.Column(models.String(32))
    identity = models.Column(models.Integer)#0学员，1教师
    identity_id = models.Column(models.Integer,nullable=True)


class Student(BaseNodel):
    #学生表
    __tablename__ = 'students'
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)#0男 1女
    to_attendance = models.relationship(
        'Attendance',#考勤的方法名
        backref = 'to_student_hh'#反向字段
    )

#多对多的关系表
Stu_Cou = models.Table(
    'stu_cou',
    models.Column("id", models.Integer, primary_key=True, autoincrement=True),
    models.Column("course_id", models.Integer, models.ForeignKey("course.id")),
    models.Column("student_id", models.Integer, models.ForeignKey("students.id"))
)
class Course(BaseNodel):
    #课程表
    __tablename__ = 'course'

    label = models.Column(models.String(32))
    description = models.Column(models.Text)
    to_teacher = models.relationship(
        'Teacher',#隐射
        backref = 'to_course_data'#反向字段teacher 查询课程的字段
    )
    to_student = models.relationship(
        'Student',#方法名
        secondary = Stu_Cou,
        backref = models.backref('to_course',lazy = 'dynamic'),#反向字段（stu_cou studens)
        lazy = 'dynamic'#(stu_cou course)
        # select 访问该字段时候，加载所有的映射数据
        # joined  对关联的两个表students和stu_cou进行join查询
        # dynamic 不加载数据
    )


class Grade(BaseNodel):
    #成绩表
    __tablename__ = 'grade'

    grade = models.Column(models.Float, default=0)
    course_id = models.Column(models.Integer, models.ForeignKey("course.id"))
    student_id = models.Column(models.Integer, models.ForeignKey("students.id"))#外键关系是学生


class Attendance(BaseNodel):
    #考勤表
    __tablename__ = 'attendance'

    att_time = models.Column(models.Date)
    status = models.Column(models.Integer, default=1)  # 0 迟到  1 正常出勤  2 早退  3 请假  4 旷课
    student_id = models.Column(models.Integer, models.ForeignKey("students.id"))#外键字段是学生表

class Teacher(BaseNodel):
    #老师表
    __tablename__ = 'teacher'

    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)  # 0 男 1女 -1 unknown
    course_id = models.Column(models.Integer, models.ForeignKey("course.id"))#外键字段的搭建对应的课程表

# models.drop_all()#删除数据库
models.create_all()#创建数据库
