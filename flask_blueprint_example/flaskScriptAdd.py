"""
flask-script添加命令
官方案例
"""
from flask import Flask
from flask_script import Manager

app = Flask(__name__)#注册app

@app.route('/')
def index():
    return '哈哈哈'
manager = Manager(app)#实例化app

@manager.command
def hello(name = 'createsuperuser'):
    """
    :param name:是命令行可以传递的参数，在命令行以 --name来传递
    :return:
    """
    username = input('输入你的用户名')
    email = input('输入你的邮箱')
    password = input('输入你的密码')
    enter_password = input('确认你的密码')
    print('恭喜{}注册成功'.format(name))
    return '这是个测试'

@manager.command
def runserver2(ip = '127.0.0.1',port=8000):
    print('runserver in %s:%s'%(ip,port))

if __name__ == '__main__':
    manager.run()#启动