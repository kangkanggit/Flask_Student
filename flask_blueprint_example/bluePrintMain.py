"""
蓝图的官方案例
注册单一的蓝图实例
使用app运行加载蓝图
"""

from flask import Flask
from flask import Blueprint

simple_blueprint = Blueprint('simple_page',__name__)#创建蓝图

#bluePrint的路由和视图
@simple_blueprint.route('/')
def index():
    return 'hhhh'

#启动项目
if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(simple_blueprint)#注册蓝图
    app.run()