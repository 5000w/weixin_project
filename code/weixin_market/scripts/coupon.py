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

###重置所有用户的优惠卷状态为启用--y有问题待修改
def update_coupon_stateTo1():
   Coupon.objects.filter().update(state=1)

#邀请的优惠卷逻辑
def share_for_coupon_(id):
    user = Weixin_user.objects.get(id=id)
    share_once_obj = user.coupon_set.get(price='share_once')

    #判断第二张优惠卷是否生效
    if share_once_obj.state == 0:

        #设置第一张生效
        share_once_obj.state = 1

        share_once_obj.save()

        return True

    #如果第一张已经生效或者，已经使用再分享的话，设置第二张优惠卷状态
    else:

        #判断第二张优惠卷的状态
        share_twice_obj = user.coupon_set.get(price='share_twice')

        #如果第二张优惠卷为0
        if share_twice_obj.state == 0:

            # 设置第2张生效
            share_twice_obj.state = 1

            share_twice_obj.save()

            return True

        #如果第二张的状态为1或者2（已经使用和可以使用）
        else:
            return False

#重置所有的优惠卷状态，慎用
def initialize_conpon_():
    cou_login = Coupon.objects.filter(price='login').update(state=1)

    cou_once = Coupon.objects.filter(price='share_once').update(state=0)

    cou_twice = Coupon.objects.filter(price='share_twice').update(state=0)

def run():
    #login_add('test1'+str(1234))
    #update_coupon(3,'login',0)
    #update_coupon_stateTo1()
    print(initialize_conpon_())