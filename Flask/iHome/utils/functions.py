import functools
from flask import session, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_ext(app):

    db.init_app(app=app)


def get_database_uri(DATABASE):

    host = DATABASE.get('HOST')
    db = DATABASE.get('DB')
    driver = DATABASE.get('DRIVER')
    port = DATABASE.get('PORT')
    user = DATABASE.get('USER')
    password = DATABASE.get('PASSWORD')
    name = DATABASE.get('NAME')

    return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver, user,
                                           password, host,
                                           port, name)


def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():

        try:
            # 验证用户是否登录
            # if session['user_id']:
            if 'user_id' in session:
                return view_fun()
            else:
                return redirect('/user/login/')
        except:
            return redirect('/user/login/')

    return decorator
