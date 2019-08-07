"""
项目管理文件，运行项目的目录
"""

from FlaskDirtory.models import models
from FlaskDirtory.views import app


if __name__ == '__main__':
    models.create_all()
    app.run(host='0.0.0.0',port=8000,debug=True)#修改配置