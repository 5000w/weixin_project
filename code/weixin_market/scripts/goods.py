from weixin.models import Weixin_user
from weixin.models import Goods

from django.utils import timezone

#添加商品到购物车
def add_goods_car(id,goods_id):

    user = Weixin_user.objects.get(id=id)
    goods = Goods.objects.get(id=goods_id)  #取到goods对象
    user.car_info_set.create(goods=goods)

#查看所有商品
def get_all_goods():
    return [{'name' : x.goods_name,'count' : x.count , 'url' : x.image_url }  for x in Goods.objects.filter()]


#查看某个openid购物车的商品
def get_goods(id):
    user = Weixin_user.objects.get(id=id)
    return [x for x in user.car_info_set.values('goods')]

#删除购物车中商品
def del_car(id,goods_id_list):

    for goods_id in goods_id_list():
        user = Weixin_user.objects.get(id=id)
        goods = Goods.objects.get(id=goods_id)
        user.car_info_set.filter(goods=goods).delete()

def run():
    #add_goods_car(3,2)
    #print(get_goods(3))
    pass

