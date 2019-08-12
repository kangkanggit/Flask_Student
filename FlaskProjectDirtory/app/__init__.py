from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_cache import Cache

import pymysql
pymysql.install_as_MySQLdb()

#惰性加载
csrf = CSRFProtect()#csf的令牌命令
models = SQLAlchemy()#对应的数据库
cache = Cache()#实例化缓存

def create_app(config_name):#创建app实例

    app = Flask(__name__)
    app.config.from_object("settings.DebugConfig")#配置文件
    # app.run(threaded = True)#对于小的项目


    #app惰性加载插件
    cache.init_app(app)#绑定app
    csrf.init_app(app) #惰性加载
    models.init_app(app)
    #注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app