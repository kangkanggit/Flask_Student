"""
flask的配置文件
"""

import os

from flask import Flask
from flask_sqlalchemy import  SQLAlchemy

app = Flask(__name__)
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#     'sqlite:///'+os.path.join(BASE_DIR,'Demo.sqlite')
# app.config['SQLALCHEMY_COMMIY_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config.from_object('config.DebugConfig')
app.config.from_pyfile('settings.py')

models = SQLAlchemy(app)#关联sqlalchemy和flask应用
