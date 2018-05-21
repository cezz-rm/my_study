import random
import re

import time
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
from rest_framework import mixins, viewsets


from HomePage.filters import CartFilter
from HomePage.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, FoodType, Goods, CartModel, \
    OrderModel, OrderGoodsModer
from HomePage.serializers import CartSerializer, allGoodsSerializer


def home(request):
    if request.method == 'GET':
        data = {
            'MainWheel': MainWheel.objects.all(),
            'MainNav': MainNav.objects.all(),
            'MainMustBuy': MainMustBuy.objects.all(),
            'MainShop': MainShop.objects.all(),
            'MainShow': MainShow.objects.all()
        }
        return render(request, 'home/home.html', {'data': data})


def market(request):
    if request.method == 'GET':
        typeid = request.GET.get('typeid', 104749)
        child = request.GET.get('childid', '0')
        sort = request.GET.get('sort')
        foodType = FoodType.objects.all()
        # 没有点击子分类child为0,则只查询主分类的, child不为0则查询子分类
        if child == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(childcid=child)
        if sort:
            if sort == '1':
                goods = goods.order_by('id')
            if sort == '2':
                goods = goods.order_by('-productnum')
            if sort == '3':
                goods = goods.order_by('-price')
            if sort == '4':
                goods = goods.order_by('price')
        # 找到子分类类名和id的字段，并处理为字典
        childTypeName = FoodType.objects.filter(typeid=typeid)
        for name in childTypeName:
            name = name.childtypenames
            childname = list(filter(None, re.split(r'[:#]', name)))
        list1, list2 = [], []
        for j in range(len(childname)):
            if j % 2 == 0:
                list1.append(childname[j])
            else:
                list2.append(childname[j])
        mydict = dict(zip(list1, list2))
        data = {
            'foodType': foodType,
            'goods': goods,
            'childname': mydict,
            'typeid': typeid,
            'childid': child,
        }
        return render(request, 'market/market.html', {'data': data})


def cart(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            carts = CartModel.objects.filter(user=user)
            return render(request, 'cart/cart.html', {'carts': carts})
    return HttpResponseRedirect('/axf/login/')


def changeSelect(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        ticket = request.COOKIES.get('ticket')
        data = {
            'code': '200',
            'msg': '请求成功',
        }
        if ticket:
            cart = CartModel.objects.filter(pk=cart_id).first()
            cart.is_select = not cart.is_select
            cart.save()
            data['is_select'] = cart.is_select
        return JsonResponse(data)


def allSelect(request):
    if request.method == 'POST':
        ticket = request.COOKIES.get('ticket')
        status = request.POST.get('status')
        data = {
            'code': '200',
            'msg': '请求成功',
        }
        if ticket:
            carts = CartModel.objects.all()
            for cart in carts:
                if status == '1':
                    cart.is_select = False
                    cart.save()
                    data['is_select'] = cart.is_select
                else:
                    cart.is_select = True
                    cart.save()
                    data['is_select'] = cart.is_select
        return JsonResponse(data)


# def change_Select(request):
#     if request.method == 'POST':
#         cart_id = request.POST.get('cart_id')
#         user = request.user
#         data = {
#
#         }
#         if user and user.id:
#             cart = CartModel.objects.filter(pk=cart_id)
#             if cart.is_select:
#                 cart.is_select = False
#             else:
#                 cart.is_select = True
#             cart.save()
#             data['is_select'] = True
#         return JsonResponse(data)


# 创建订单
def generateOrder(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            # 查询is_select为True的
            carts_goods = CartModel.objects.filter(is_select=True)
            # 创建订单
            order = OrderModel.objects.create(user=user, o_status=0)
            # 创建订单详情信息
            for carts in carts_goods:
                OrderGoodsModer.objects.create(goods=carts.goods,
                                               order=order,
                                               goods_num=carts.c_num)
            carts_goods.delete()
            return HttpResponseRedirect(reverse('axf:payOrder', args=(str(order.id),)))


# 订单状态
def payOrder(request, order_id):
    if request.method == 'GET':
        orders = OrderModel.objects.get(pk=order_id)
        ordergoods = orders.ordergoodsmoder_set.all()
        data = {
            'order_id': order_id,
            'order': orders,
            'ordergoods': ordergoods
        }
        return render(request, 'order/order_info.html', data)


# 完成支付
def payed(request, order_id):
    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect('/axf/mine/')


# 待付款
def orderWaitPay(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            orders = OrderModel.objects.filter(user=user, o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


# 待收货
def waitShouhuo(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            orders = OrderModel.objects.filter(user=user, o_status=1)
            return render(request, 'order/order_list_payed.html', {'orders': orders})


def mine(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            orders = user.ordermodel_set.all()
            wait_pay, already_pay = 0, 0
            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    already_pay += 1
            data = {
                'user': user,
                'wait_pay': wait_pay,
                'already_pay': already_pay
            }
            return render(request, 'mine/mine.html', data)
        else:
            return render(request, 'mine/mine.html')


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            icon=icon
        )
        return HttpResponseRedirect('/axf/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                s = 'abcdefghijklmnopqlstuvwxyz'
                ticket = ''
                for i in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK_' + ticket + str(now_time)
                response = HttpResponseRedirect('/axf/mine/')
                # out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, max_age=6000)
                user.ticket = ticket
                user.save()
                return response
            else:
                # 用户密码错误
                return HttpResponseRedirect('/axf/login/')
        else:
            # 用户不存在
            return HttpResponseRedirect('/axf/regist/')


def logout(request, id):
    if request.method == 'GET':
        user = UserModel.objects.get(id=id)
        response = HttpResponseRedirect('/axf/mine/')
        response.delete_cookie('ticket')
        user.ticket = ''
        user.save()
        # ticket = request.COOKIES.get('ticket')
        # UserModel.objects.get(ticket=ticket).delete()
        return response


def addgoods(request):
    if request.method == 'POST':
        ticket = request.COOKIES.get('ticket')
        data = {
            'code': '200',
            'msg': '请求成功',
        }
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            good_id = request.POST.get('good_id')
            user_carts = CartModel.objects.filter(user=user, goods_id=good_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user_id=user.id,
                                         goods_id=good_id,
                                         c_num=1)
                data['c_num'] = 1
            return JsonResponse(data)


def subgoods(request):
    if request.method == 'POST':
        ticket = request.COOKIES.get('ticket')
        data = {
            'code': '200',
            'msg': '请求成功',
        }
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            good_id = request.POST.get('good_id')
            user_carts = CartModel.objects.filter(user_id=user.id,
                                                  goods_id=good_id).first()
            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
            else:
                pass
        return JsonResponse(data)


def add_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200,
        }
        user = request.user
        if user and user.id:
            good_id = request.POST.get('good_id')
            user_carts = CartModel.objects.filter(user=user, goods_id=good_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user=user,
                                         goods_id=good_id,
                                         c_num=1)
            data['c_num'] = 1
            return JsonResponse(data)


def sub_goods(request):
    if request.method == 'POST':
        data = {
            'code': '200',
            'msg': '请求成功'
        }
        user = request.user
        good_id = request.POST.get('good_id')
        if user and user.id:
            user_carts = CartModel.objects.filter(user=user,
                                                  goods_id=good_id)
            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
        return JsonResponse(data)


class CartEdit(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    # 查询所有数据
    queryset = CartModel.objects.all()
    # 序列化有所有数据(按一定格式返回)
    serializer_class = CartSerializer
    # 过滤
    # filter_class = CartFilter


# class allGoodsEdit(mixins.ListModelMixin,
#                mixins.RetrieveModelMixin,
#                mixins.UpdateModelMixin,
#                mixins.DestroyModelMixin,
#                mixins.CreateModelMixin,
#                viewsets.GenericViewSet):
#     # 查询所有数据
#     queryset = Goods.objects.all()
#     # 序列化有所有数据(按一定格式返回)
#     serializer_class = allGoodsSerializer
#
#     # filter_class = CartFilter
#
#     def get_queryset(self):
#         goods_id = self.request.query_params['goods_id']
#         query = self.queryset.filter(id=goods_id)
#
#         return query