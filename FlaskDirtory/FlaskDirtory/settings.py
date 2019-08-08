import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI=\
    'sqlite:///'+os.path.join(BASE_DIR, 'Demo.sqlite')#dem.sqlite是库名
SQLALCHEMY_COMMIY_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True