from weixin.models import Weixin_user
from weixin.models import Class_info
from .zhihuishu import *

from django.utils import timezone
import time

#添加订单，目前订单默认为已付款状态
'''
class name 使用数组传入，在后端转换为字符串
phone_number 使用字符串传入，中间用 ， 隔开
type 1 为智慧树，2 为超星
'''
###class_name_list是一个数组
def add_order(id,price,class_name_list,phone_number,pwd,type,school_name=''):
    cname = ','.join(class_name_list)
    user = Weixin_user.objects.get(id=id)
    order_info =user.order_info_set.create(state = 'PAY',price = price)
    order_info.class_info_set.create(class_name = cname,phone_number=phone_number,pwd=pwd,school_name=school_name,type=type)


#获得个人的order信息
'''
1、先从数据库查询已经下单的课
2、拿到账号去超星和智慧树查询
3、查询后自己的classname比较
'''
def get_order(id):
    user = Weixin_user.objects.get(id=id)
    order_info = user.order_info_set.filter()
    data_list=[]
    for x in order_info:
        res = x.class_info_set.filter()
        if res.exists() :
            res =res[0]
            data_list.append({'type' : res.type,'class_name' : res.class_name ,'phone_number' : res.phone_number,'pwd' : res.pwd, 'school_name' : res.school_name})
    total_list=[]
    #首先遍历数据库里面的订单
    for i in data_list:
        if i['type'] == 1: #智慧树
            classlist= i['class_name'].split(',')
            return_list = get_data(i['phone_number'], i['pwd'])['data']
            #把数据库里面的class_name进行遍历 找到对应的百分比
            for class_in_db in classlist:
                for class_in_api in return_list:
                    if class_in_api['courseName'] == class_in_db:
                        total_list.append(class_in_api)
                        break

        else:
            #调取超新的接口 还没写
            print(1)
    print(data_list)
    print(total_list)
#提供导出成txt 的接口
def get_order_bytxt():
    class_info =Class_info.objects.filter()

    file = open("./txt/data.txt", "w")
    count=0
    for x in class_info:
        if x.type == 1 :
            file.write("{4} {0} {1} {2} {3}\n".format(x.school_name,x.phone_number,x.pwd,x.class_name,'智慧树'))
            count=count+len(x.class_name.split(','))
        else:
            file.write("{4} {0} {1} {2} {3}\n".format(x.school_name, x.phone_number, x.pwd, x.class_name, '超星'))
            count = count + len(x.class_name.split(','))
    file.write("总计："+ str(count) )
    file.close()
def run():
    #add_order(1,100,['ca1','ca2','ce3','cessssssss'],'18581566204','pwd',1)
    #add_order(1, 10, ['现代市场营销素质与能力提升'], '17391314633', 'll19971017', 1,)
    get_order(1)