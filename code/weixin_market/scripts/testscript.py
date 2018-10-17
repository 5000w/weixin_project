##优惠卷
from weixin.models import Weixin_user
from weixin.models import Coupon
from weixin_market.settings import *
from django.utils import timezone
import requests
import time
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
    #login_test('test144'+str(1234))
    #login_add_coupon('test')
    list1 = [{'courseName': '现代市场营销素质与能力提升', 'planProgress': '5.6%'},{'....'},{'....'}]
    list2 = ['现代市场营销素质与能力提升','现代市场营销素质与能力提升']
    a = int(time.time())
    class_data_list =[{
		'type' : 1,          #int    1为智慧树 2为超星
		'phone_number' : '13325465996', #电话号码
		'pwd' : 'fzh19971115',       #密码
		'school_name' : '西安财经学院行知学院' ,#学校名称
		'class_name' : ['关爱生命——急救与自救技能','女生穿搭技巧','上大学，不迷茫','教你成为歌唱达人','不负卿春-大学生职业生涯规划']  #class_name
	},
        {
            'type': 1,  # int    1为智慧树 2为超星
            'phone_number': '18690489289',  # 电话号码
            'pwd': '980708',  # 密码
            'school_name': '西安财经学院行知学院',  # 学校名称
            'class_name': ['关爱生命——急救与自救技能', '女生穿搭技巧', '上大学，不迷茫', '教你成为歌唱达人', '不负卿春-大学生职业生涯规划','创业营销——创业新手营销实战指南','高级英语写作']  # class_name
        }
    ]
    # r = requests.post("https://www.saber-toothed.xyz/wx/add_order",
    #                   headers={'openid': 'onAnm5apw-wPIaInTC_c45ZjLRl8', 'time': '1538243507'},
    #                   json={'price': 9.9, 'class_data_list': class_data_list})

    # r = requests.post("https://www.saber-toothed.xyz/wx/get_class",
    #                   headers={'openid': 'onAnm5apw-wPIaInTC_c45ZjLRl8', 'time': '1538243507'},
    #                   json={'type': 1, 'phone_number': '18690489289','pwd':'980708'})

    r = requests.post("https://www.saber-toothed.xyz/wx/get_order_detail",
                      headers={'openid': 'onAnm5apw-wPIaInTC_c45ZjLRl8', 'time': '1538243507'},
                      json={})
    print(r.json())