import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SQLALCHEMY_COMMIY_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(BASE_DIR, 'Demo.sqlite')

class OnlineConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(BASE_DIR, 'Demo.sqlite')