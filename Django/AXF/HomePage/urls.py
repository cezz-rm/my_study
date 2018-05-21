from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from HomePage import views

router = SimpleRouter()
router.register(r'^myrest', views.CartEdit)
# router.register(r'^allgoods',views.allGoodsEdit)

urlpatterns =[
    url(r'home/', views.home, name='home'),
    url(r'market/', views.market, name='market'),
    url(r'cart/', views.cart, name='cart'),
    url(r'mine/', views.mine, name='mine'),
    url(r'login/', views.login, name='login'),
    url(r'regist/', views.regist, name='regist'),
    url(r'logout/(?P<id>\d+)', views.logout, name='logout'),
    url(r'^addgoods/', views.addgoods, name='addgoods'),
    url(r'^subgoods/', views.subgoods, name='subgoods'),
    url(r'^changeCartSelect/', views.changeSelect, name='changeCartSelect'),
    url(r'^allSelect/', views.allSelect, name='allSelect'),
    url(r'^generateOrder/', views.generateOrder, name='generateOrder'),
    url(r'^payOrder/(\d+)/', views.payOrder, name='payOrder'),
    url(r'^payed/(\d+)/', views.payed, name='payed'),

    url(r'^orderWaitPay/', views.orderWaitPay, name='orderWaitPay'),
    url(r'^waitShouhuo/', views.waitShouhuo, name='waitShouhuo'),
]


urlpatterns += router.urls
