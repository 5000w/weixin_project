##优惠卷
from weixin.models import Weixin_user
from weixin.models import Coupon
from weixin_market.settings import *
from django.utils import timezone
import pdb
logger = logging.getLogger("weixin.views")
###test
def login_test(open_id):
    logger.info(5345)
    logger.error(74)
    logger.warning("fasdfd")
    logger.debug("[Debug] "+"已有用户")
    obj = Weixin_user(openid="公的司6gfs6梵00656")
    obj.save()
    #print(obj.id)

####注册时给用户添加优惠卷
def login_add_coupon(openid):
    user = Weixin_user.objects.get(openid=openid)
    user.coupon_set.create(price='login',state=1,start_time=timezone.now())
    user.coupon_set.create(price='share_once',state=1,start_time=timezone.now())
    user.coupon_set.create(price='share_twice',state=1,start_time=timezone.now())
    print(user.coupon_set.count())

def run():
    login_test('test144'+str(1234))
    #login_add_coupon('test')