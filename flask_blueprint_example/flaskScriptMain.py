"""
官方案例
"""

from flask import Flask
from flask_script import Manager#引入命令

app = Flask(__name__)

@app.route('/index/')
def index():
    return 'Hello world'


manager = Manager(app)#注册app

if __name__ == '__main__':
    manager.run()#用命令启动