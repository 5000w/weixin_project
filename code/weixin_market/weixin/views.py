import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .config import CODE2SESSION, Order_url
from .models import Weixin_user
from .login_interface.login_operation import write_login_header, generate_header_value , check_header
import requests
from weixin_market.settings import *
from scripts.coupon import *
from . import pay
from scripts import *

# Create your views here.
logger = logging.getLogger("weixin.view")


def user_login(request):
    get_data = json.loads(request.body)
    codeurl = CODE2SESSION.substitute({'CODE': get_data['js_code']})
    result = json.loads(requests.get(codeurl).text)
    try:
        if Weixin_user.objects.filter(openid=result["openid"]):
            logger.error("已有用户")
        else:

            Weixin_user(openid=result["openid"]).save()
            login_add_coupon(result["openid"])  # 优惠卷初始化
    except KeyError:
        logger.error(f'error code cant get openid')
        return JsonResponse({"succ": False, "msg": "get openid fault", "data": {}})
    header_info = generate_header_value(result["openid"])
    write_login_header(result["openid"], header_info)  # 写入redis登陆header

    re_json = {"succ": True, "msg": "", "data": header_info}
    return JsonResponse(re_json)

# 统一下单支付接口


def payOrder(request, user_id):
    import time
    if request.method == 'POST':
        # 获取价格
        price = request.POST.get("price")

        # 获取客户端ip
        client_ip, port = request.get_host().split(":")

        # 获取小程序openid
        openid = Weixin_user.objects.get(openid=user_id).openid

        # 请求微信的url
        url = Order_url

        # 拿到封装好的xml数据
        body_data = pay.get_bodyData(openid, client_ip, price)

        # 获取时间戳
        timeStamp = str(int(time.time()))

        # 请求微信接口下单
        respone = requests.post(url, body_data.encode(
            "utf-8"), headers={'Content-Type': 'application/xml'})

        # 回复数据为xml,将其转为字典
        content = pay.xml_to_dict(respone.content)

        if content["return_code"] == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content.get("prepay_id")
            # 获取随机字符串
            nonceStr = content.get("nonce_str")

            # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr)

            # 封装返回给前端的数据
            data = {"prepay_id": prepay_id, "nonceStr": nonceStr,
                    "paySign": paySign, "timeStamp": timeStamp}

            return JsonResponse(data)

        else:
            return JsonResponse({"请求支付失败": 434})
    else:
        return JsonResponse({"msg": "请求方法错误"})


 
def payback(request):
    msg = request.body.decode('utf-8')
    xmlmsg = pay.xml_to_dict(msg)
 
    return_code = xmlmsg['return_code']
 
    if return_code == 'FAIL':
        # 官方发出错误
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                            <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                            content_type='text/xml', status=200)
    elif return_code == 'SUCCESS':
        # 拿到这次支付的订单号
        out_trade_no = xmlmsg['xml']['out_trade_no']
 
        # 根据需要处理业务逻辑
 
        return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                            <return_msg><![CDATA[OK]]></return_msg></xml>""",
                            content_type='text/xml', status=200)

def get_id():
    pass

@check_header
def get_coupon(request):
    id = get_id()
    list = get_coupon_db(id)
    re_json = {"succ": True, "msg": "操作成功", "data": {'list' : list}}
    return JsonResponse(re_json)


@check_header
def set_coupon_sta(request):
    id = get_id()
    get_data = json.loads(request.body)
    update_coupon(id,get_data['price'],get_data['state'])
    re_json = {"succ": True, "msg": "操作成功", "data": {}}
    return JsonResponse(re_json)

