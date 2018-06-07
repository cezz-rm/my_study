import os
from flask import Blueprint, render_template, jsonify, session, request
from sqlalchemy import or_

from iHome.models import User, House, Area, Facility, db, HouseImage, Order
from utils import status_code
from utils.settings import UPLOAD_DIRS

house_blueprint = Blueprint('house', __name__)


# 我的房源
@house_blueprint.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


# 我的房源信息api
@house_blueprint.route('/auth_myhouse/', methods=['GET'])
def auth_myhouse():

    user = User.query.get(session['user_id'])
    if user.id_card:

        houses = House.query.filter(House.user_id == user.id).order_by(House.id.desc())
        house_list = []
        for house in houses:
            house_list.append(house.to_dict())
        return jsonify(house_list=house_list, code=status_code.OK, user=user.id_card)

    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


# 发布新房源
@house_blueprint.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


# 发布新房源接口, 获取area地区, facility设备信息
@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilitys = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilitys]

    return jsonify(area_list=area_list, facility_list=facility_list)


# 发布新房源接口, POST请求
@house_blueprint.route('/my_new_house/', methods=['POST'])
def my_new_house():

    house_dict = request.form
    # 基本信息
    title = house_dict.get('title')
    price = house_dict.get('price')
    area_id = house_dict.get('area_id')
    address = house_dict.get('address')

    # 详细信息
    room_count = house_dict.get('room_count')
    acreage = house_dict.get('acreage')
    unit = house_dict.get('unit')
    capacity = house_dict.get('capacity')
    beds = house_dict.get('beds')
    deposit = house_dict.get('deposit')
    min_days = house_dict.get('min_days')
    max_days = house_dict.get('max_days')

    # 配套设施
    facilitys = house_dict.getlist('facility')

    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(status_code.MYHOUSE_INFO_IS_NOT_FULL)

    user = User.query.get(session['user_id'])
    house = House()
    house.user_id = user.id
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = max_days
    house.max_days = max_days

    try:
        house.add_update()
        hou = House.query.get(house.id)
        for facility in facilitys:
            fac = Facility.query.get(facility)
            hou.facilities.append(fac)
            db.session.add(hou)
        db.session.commit()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


# 发布新房源接口文字信息, POST请求
@house_blueprint.route('/newhouse/', methods=['POST'])
def user_newhouse():

    house_dict = request.form.to_dict()
    facility_ids = request.form.getlist('facility')

    house = House()
    house.user_id = session['user_id']
    # 基本信息
    house.title = house_dict.get('title')
    house.price = house_dict.get('price')
    house.area_id = house_dict.get('area_id')
    house.address = house_dict.get('address')

    # 详细信息
    house.room_count = house_dict.get('room_count')
    house.acreage = house_dict.get('acreage')
    house.unit = house_dict.get('unit')
    house.capacity = house_dict.get('capacity')
    house.beds = house_dict.get('beds')
    house.deposit = house_dict.get('deposit')
    house.min_days = house_dict.get('min_days')
    house.max_days = house_dict.get('max_days')

    if facility_ids:
        facilitys = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facilitys
    try:
        house.add_update()
        return jsonify(code=status_code.OK, house_id=house.id)

    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


# 发布新房源接口图片信息, POST请求
@house_blueprint.route('/images/', methods=['POST'])
def newhouse_images():

    images = request.files.get('house_image')
    house_id = request.form.get('house_id')

    # 保存成功
    url = os.path.join(UPLOAD_DIRS, images.filename)
    images.save(url)

    image_url = os.path.join(os.path.join('\static', 'upload'), images.filename)
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image_url
    try:
        house_image.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    house = House.query.get(house_id)

    if not house.index_image_url:

        house.index_image_url = image_url
        try:
            house.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.OK, image_url=image_url)


# 房间信息
@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):

    house = House.query.get(id)

    facility_list = house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]

    booking = 1
    if 'user_id' in session:
        house.user_id = session['user_id']
        booking = 0
    return jsonify(house=house.to_full_dict(),
                   facility_list=facility_dict_list,
                   booking=booking,
                   code=status_code.OK)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@house_blueprint.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@house_blueprint.route('/hindex/', methods=['GET'])
def house_index():

    user_name = ''

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   user_name=user_name,
                   hlist=hlist,
                   alist=alist)


@house_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blueprint.route('/allsearch/', methods=['GET'])
def house_search():

    search_dict = request.args

    area_id = search_dict.get('aid')
    start_date = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_key = search_dict.get('sk')

    if area_id:
        houses = House.query.filter(House.area_id == area_id)
    else:
        houses = House.query

    # 对房屋house进行处理
    orders1 = Order.query.filter(Order.begin_date >= start_date,
                       Order.end_date <= end_date)

    orders2 = Order.query.filter(Order.begin_date <= end_date,
                       Order.end_date >= end_date)

    orders3 = Order.query.filter(Order.begin_date <= start_date,
                       Order.end_date >= start_date)

    orders4 = Order.query.filter(Order.begin_date <= start_date,
                       Order.end_date >= end_date)

    orders_list1 = [o1.house_id for o1 in orders1]
    orders_list2 = [o2.house_id for o2 in orders2]
    orders_list3 = [o3.house_id for o3 in orders3]
    orders_list4 = [o4.house_id for o4 in orders4]

    orders_list = orders_list1 + orders_list2 + orders_list3 + orders_list4
    orders_list = list(set(orders_list))

    houses = houses.filter(House.id.notin_(orders_list))

    if sort_key:
        if sort_key == 'new':
            sort_key = House.create_time.desc()
            sort_name = '最新上线'
        if sort_key == 'booking':
            sort_key = House.room_count.desc()
            sort_name = '入住最多'
        if sort_key == 'price-inc':
            sort_key = House.price.asc()
            sort_name = '价格 低-高'
        if sort_key == 'price-des':
            sort_key = House.price.desc()
            sort_name = '价格 高-低'
    else:
        sort_key = House.create_time.desc()
        sort_name = '最新上线'

    houses = houses.order_by(sort_key)

    hlist = [house.to_full_dict() for house in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    area_name = Area.query.filter(Area.id == area_id).first().name if area_id else '位置区域'

    return jsonify(code=status_code.OK,
                   hlist=hlist,
                   alist=alist,
                   area_name=area_name,
                   sort_name=sort_name)