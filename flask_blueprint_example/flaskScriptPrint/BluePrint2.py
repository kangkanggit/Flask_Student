"""
多蓝图模式
"""

from flask import Blueprint

simple_blueprint2 = Blueprint('simple_page1',__name__)#窗建蓝图

#bluePrint的路由和视图
@simple_blueprint2.route('/index1/')
def index():
    return 'hello world1'