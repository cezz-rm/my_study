import os

from utils.functions import get_database_uri

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_dir = os.path.join(BASE_DIR, 'static')

templates_dir = os.path.join(BASE_DIR, 'templates')

DATABASE = {
    'USER': 'root',
    'PASSWORD': '482185',
    'HOST': 'localhost',
    'PORT': '3306',
    'DB': 'mysql',
    'DRIVER': 'pymysql',
    'NAME': 'ihome'
}

SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

UPLOAD_DIRS = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
