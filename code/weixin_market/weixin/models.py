from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

#微信user
class Weixin_user(models.Model):
    openid = models.CharField(max_length=50,unique=True)             #微信用户的openid
    start_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

#账户信息
class Account_info(models.Model):
    weixin_user = models.ForeignKey(Weixin_user,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)             #账号的手机号
    password = models.CharField(max_length=50) #账户的密码

#优惠卷
class Coupon(models.Model):
    weixin_user = models.ForeignKey(Weixin_user,on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  #优惠卷生成的时间
    price_choice = (
        ("login","29-5"),
        ("share_once","99-19"),
        ("share_twice","149-39"),
    )
    price = models.CharField(max_length=20,choices=price_choice)  #3中订单的状态
    state = models.IntegerField(default=1)

#订单
class Order_info(models.Model):
    state_choice = (
        ("CLOSE","已取消"),
        ("GENERATE","已生成"),
        ("PAY","已付款"),
    )
    weixin_user = models.ForeignKey(Weixin_user, on_delete=models.CASCADE,default=None)
    start_time = models.DateTimeField(auto_now_add=True)                         #生成的时间
    update_time = models.DateTimeField(auto_now=True)                            #更新时间
    state = models.CharField(max_length=50,choices=state_choice,default="CLOSE") #订单的状态
    price = models.FloatField(default=9.9)                                       #订单的最终价格
    generate_info = models.CharField(max_length=1000)                            #上传的刷课数据，后面用于导出

#课程
class Class_info(models.Model):
    order_id = models.ForeignKey(Order_info,on_delete=models.CASCADE,default=None) #订单id
    class_name = models.CharField(max_length=1000)    #课程的名字
    class_percent = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)]) #课程的百分比
    phone_number = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50,default=None)
    school_name = models.CharField(max_length=50,default=None)
    type = models.IntegerField(default=0) #1为智慧树 2为超星

#商品
class Goods(models.Model):
    goods_name = models.CharField(max_length=50)  # 商品名字
    count = models.IntegerField(default=0)
    image_url = models.CharField(max_length=100,default=None)

class Car_info(models.Model):
    goods= models.ForeignKey(Goods,on_delete=models.CASCADE,default=None)  # 购物车
    weixin_user = models.ForeignKey(Weixin_user, on_delete=models.CASCADE)


# class Goods(models.Model):
#     goods_name = models.CharField(max_length=50)
#     goods_count = models.IntegerField(default=0)
#
# class Shopping_car(models.Model):
#     user_id = models.ForeignKey(Weixin_user,on_delete=models.CASCADE)
#     good_id