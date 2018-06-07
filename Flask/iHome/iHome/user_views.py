import re

import os
from flask import Blueprint, render_template, request, jsonify, session, redirect

from iHome.models import db, User
from utils import status_code
from utils.functions import is_login
from utils.settings import UPLOAD_DIRS

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello_user():
    return '欢迎'


@user_blueprint.route('/createdb/')
def create_db():
    db.create_all()
    return '创建数据库成功'


# 注册页面
@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 注册api
@user_blueprint.route('/register/', methods=['POST'])
def user_register():

    register_dict = request.form

    mobile = register_dict.get('mobile')
    password = register_dict.get('password')
    password2 = register_dict.get('password2')

    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    if User.query.filter(User.phone == mobile).count():
        return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXISTS)

    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password
    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


# 登录页面
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 登录api
@user_blueprint.route('/login/', methods=['POST'])
def user_login():

    user_dict = request.form

    mobile = user_dict.get('mobile')
    password = user_dict.get('password')
    # 用户未登录从浏览好的房源登录时
    house_id = user_dict.get('house_id')

    if not all([mobile, password]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    user = User.query.filter(User.phone == mobile).first()
    if user:
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(code=status_code.OK, house_id=house_id)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXISTS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 用户信息显示api
@user_blueprint.route('/user/', methods=['GET'])
@is_login
def get_user_profile():

    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict(), code=200)


@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


# 用户头像修改api
@user_blueprint.route('/user/', methods=['PUT'])
@is_login
def user_profile():

    user_dict = request.form
    file_dict = request.files
    if 'avatar' in file_dict:
        f1 = file_dict['avatar']

        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)

        url = os.path.join(UPLOAD_DIRS, f1.filename)

        f1.save(url)

        user = User.query.filter(User.id == session['user_id'])
        image_url = os.path.join('/static/upload/', f1.filename)
        user.first().avatar = image_url
        try:
            user.first().add_update()
            return jsonify(code=status_code.OK, url=image_url)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)

    elif 'name' in user_dict:
        name = user_dict.get('name')
        if User.query.filter(User.name == name).count():
            return jsonify(status_code.USER_NAME_IS_EXISTS)

        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)

    else:
        return jsonify(status_code.PARAMS_ERROR)


# 实名认证
@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():
    user = User.query.get(session['user_id'])
    if user.id_name != None and user.id_card != None:
        return jsonify(code=status_code.OK,
                       id_name=user.id_name,
                       id_card=user.id_card)
    else:
        return jsonify(code=1000, msg='没有实名认证信息')


# 实名认证api
@user_blueprint.route('/auths/', methods=['PUT'])
@is_login
def user_auth():

    user_dict = request.form
    id_name = user_dict.get('real_name')
    id_card = user_dict.get('id_card')

    if not all([id_name, id_card]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_IS_ERROR)

    try:
        user = User.query.get(session['user_id'])
        user.id_card = id_card
        user.id_name = id_name

        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/logout/')
@is_login
def user_logout():
    session.clear()
    return jsonify(status_code.SUCCESS)

