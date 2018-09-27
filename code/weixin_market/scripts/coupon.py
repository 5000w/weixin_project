##优惠卷
from weixin.models import Weixin_user
from weixin.models import Coupon

from django.utils import timezone

import  pdb

###test
def login_test(open_id):
    obj = Weixin_user(openid=open_id)
    obj.save()
    print(obj.id)

####注册时给用户添加优惠卷
def login_add_coupon(openid):
    user = Weixin_user.objects.get(openid=openid)
    user.coupon_set.create(price='login',state=1)
    user.coupon_set.create(price='share_once',state=0,start_time=timezone.now())
    user.coupon_set.create(price='share_twice',state=0,start_time=timezone.now())

###设置优惠卷的状态
def update_coupon(id,price,state):
    user = Weixin_user.objects.get(id=id)
    user.coupon_set.filter(price=price).update(state=state)

##查看某个用户的优惠卷状态
def get_coupon_db(id):
    user = Weixin_user.objects.get(id=id)
    return [{'price' : obj.price,'state' : obj.state} for obj in user.coupon_set.filter()]

###重置所有用户的优惠卷状态为启用
def update_coupon_stateTo1():
   Coupon.objects.filter().update(state=1)



def run():
    pass
    #login_add('test1'+str(1234))
    #update_coupon(3,'login',0)
    #update_coupon_stateTo1()