from weixin.models import Weixin_user
from weixin.models import Class_info
from .zhihuishu import *

import re


from django.utils import timezone
import time

#添加订单，目前订单默认为已付款状态
'''
class name 使用数组传入，在后端转换为字符串
phone_number 使用字符串传入，中间用 ， 隔开
type 1 为智慧树，2 为超星
'''

###class_name_list是一个数组
def add_order_(id,price,class_data_list):

    user = Weixin_user.objects.get(id=id)
    order_info =user.order_info_set.create(state = 'PAY',price = price)

    #将class_name_list 中的值存入数据库class info，使用的为一个order id
    for data in class_data_list:
        class_name_list = data['class_name']
        cname = ','.join(class_name_list)
        order_info.class_info_set.create(class_name = cname ,phone_number=data['phone_number'],pwd=data['pwd'],school_name=data['school_name'],type=data['type'])


#获得个人的order信息
'''
1、先从数据库查询已经下单的课
2、拿到账号去超星和智慧树查询
3、查询后自己的classname比较
'''
def get_order(id):
    #根据用户找到user obj
    user = Weixin_user.objects.get(id=id)

    #找到这个用户的所有订单
    order_info = user.order_info_set.filter()

    data_list=[]

    #循环所有的订单
    for x in order_info:
        #每个订单有多个class_info
        res_ = x.class_info_set.filter()
        #如果这个订单存在class,就将每条class 存到data_list里面
        if res_.exists() :
            for class_data in res_:
                res = class_data
                data_list.append({'type' : res.type,'class_name' : res.class_name ,'phone_number' : res.phone_number,'pwd' : res.pwd, 'school_name' : res.school_name})

    total_list=[]

    #首先遍历数据库里面的class信息，从上面写循环得到完整的data_list
    for i in data_list:
        if i['type'] == 1:  #智慧树
            classlist= i['class_name'].split(',')
            return_list = get_data_by_zhihuishu(i['phone_number'], i['pwd'])['data']

            #把数据库里面的class_name进行遍历 找到对应的百分比
            for class_in_db in classlist:
                for class_in_api in return_list:
                    if class_in_api['courseName'] == class_in_db:
                        total_list.append(class_in_api)
                        break

        else:
            #调取超新的接口 还没写
            print("")

    return total_list
#提供导出成txt 的接口
def get_order_bytxt():
    class_info =Class_info.objects.filter(class_percent=0)

    with open('./txt/data.txt', 'a') as file:
        count=0
        for x in class_info:
            if x.type == 1 :
                file.write("{4} {0} {1} {2} {3}\r\n".format(x.school_name,x.phone_number,x.pwd,x.class_name,'智慧树'))
                count=count+len(x.class_name.split(','))

            else:
                file.write("{4} {0} {1} {2} {3}\r\n".format(x.school_name, x.phone_number, x.pwd, x.class_name, '超星'))
                count = count + len(x.class_name.split(','))

        file.write("总计：{0} \r\n".format(count))
        file.write("---------------------------------------------------------\r\n")

        file.close()

    #设置一个标识字段，使用暂时没有用的class_percent字段作为标识字段
    #默认为0，设置为1，为统计过的条数
    class_info.update(class_percent='1')


def run():

    lis =[{
		'type' : 1,          #int    1为智慧树 2为超星
		'phone_number' : '', #电话号码
		'pwd' : 'pwd',       #密码
		'school_name' : '垃圾大学' ,#学校名称
		'class_name' : ['关爱生命——急救与自救技能','女生穿搭技巧']  #class_name
	},{
		'type' : 1,          #int    1为智慧树 2为超星
		'phone_number' : '', #电话号码
		'pwd' : 'pwd',       #密码
		'school_name' : '垃圾大学' ,#学校名称
		'class_name' : ['关爱生命——急救与自救技能','女生穿搭技巧']  #class_name
	},{
		'type' : 1,          #int    1为智慧树 2为超星
		'phone_number' : '', #电话号码
		'pwd' : 'pwd',       #密码
		'school_name' : '垃圾大学' ,#学校名称
		'class_name' : ['关爱生命——急救与自救技能','女生穿搭技巧']  #class_name
	},
	]
    #add_order_(4,9.9,lis)
    print(get_order_bytxt())
