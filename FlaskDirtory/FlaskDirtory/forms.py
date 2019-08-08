import wtforms #定义字段
from flask_wtf  import  Form#定义表的父类
from  wtforms import validators#定义效验
from FlaskDirtory.models import Course

course_list = [(i.id,i.label) for i in Course.query.all()]
class TeacherForm(Form):
    """
        form字段的参数
        label=None, 表单的标签
        validators=None, 校验，传入校验的方法
        filters=tuple(), 过滤
        description='',  描述
        id=None, html id
        default=None, 默认值
        widget=None,
        render_kw=None,
        """
    name = wtforms.StringField('教师姓名',
                               render_kw={
                               'class':'form-control',
                                'placeholder':'教师姓名'#提示框的内容
                               },
                               validators = [
                                   validators.DataRequired('姓名不为空')
                               ]
                               )
    age = wtforms.IntegerField('教师年龄',
                               render_kw={
                                   'class':'form-control',
                                   'placeholder':'教师年龄'#提示框的内容
                               },
                               validators = [
                                   validators.DataRequired('年龄不可以为空')
                               ]
                               )
    gender = wtforms.SelectField('性别',
                                 choices=[
                                     ('1','男'),
                                     ('2','女')
                                 ],
                                 render_kw={
                                     'class':'form-control',
                                 },
                                 )
    course = wtforms.SelectField(
        '学科',
        choices=course_list,
        render_kw={
            "class": "form-control",
        }
    )