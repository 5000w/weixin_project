#coding=utf-8
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .config import CODE2SESSION, Order_url
from .models import Weixin_user
from .login_interface.login_operation import write_login_header, generate_header_value , check_header ,get_id_by_openid
import requests
from weixin_market.settings import *
from scripts.coupon import *
from scripts.order import *
from scripts.goods import *
from . import pay
from scripts.zhihuishu import *
from scripts import *
import pdb
from django.http import StreamingHttpResponse

# Create your views here.
logger = logging.getLogger("weixin.view")


def user_login(request):
    get_data = json.loads(request.body)
    codeurl = CODE2SESSION.substitute({'CODE': get_data['js_code']})
    result = json.loads(requests.get(codeurl).text)
    try:
        if Weixin_user.objects.filter(openid=result["openid"]):
            logger.info("已有用户")
        else:
            Weixin_user(openid=result["openid"]).save()
            login_add_coupon(result["openid"])  # 优惠卷初始化
    except KeyError:
        logger.error(f'error code cant get openid')
        return JsonResponse({"succ": False, "msg": "get openid fault", "data": result})
    header_info = generate_header_value(result["openid"])
    write_login_header(result["openid"], header_info)  # 写入redis登陆header

    re_json = {"succ": True, "msg": "", "data": header_info}
    return JsonResponse(re_json)

# 统一下单支付接口


def payOrder(request):
    import time
    if request.method == 'POST':
        price = json.loads(request.body)["price"] # 获取价格
        price = round(price)
        client_ip = request.META["HTTP_X_REAL_IP"] # 获取客户端ip
        #openid = "onAnm5WbhguBA6qhbbg1f7N_zYxA"
        openid = request.META["HTTP_OPENID"] # 获取小程序openid
        url = Order_url # 请求微信的url
        body_data = pay.get_bodyData(openid, client_ip, price) # 拿到封装好的xml数据
        timeStamp = str(int(time.time())) # 获取时间戳
        respone = requests.post(url, body_data.encode(
            "utf-8"), headers={'Content-Type': 'application/xml'}) # 请求微信接口下单
        content = pay.xml_to_dict(respone.content) # 回复数据为xml,将其转为字典
        if content["return_code"] == 'SUCCESS':
            prepay_id = "prepay_id="+content.get("prepay_id") # 获取预支付交易会话标识
            nonceStr = content.get("nonce_str") # 获取随机字符串
            paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr) # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            data = {"prepay_id": prepay_id, "nonceStr": nonceStr,
                    "paySign": paySign, "timeStamp": timeStamp} # 封装返回给前端的数据
            return JsonResponse({"succ":True,"data":data,"msg":"succ"})
        else:
            return JsonResponse({"请求支付失败": 434})
    else:
        return JsonResponse({"msg": "请求方法错误"})


 
def payback(request):
    msg = request.body.decode('utf-8')
    xmlmsg = pay.xml_to_dict(msg)
    return_code = xmlmsg['return_code']
    if return_code == 'FAIL':
        # 官方发出错误 + 支付失败
        print(xmlmsg)
        #错误逻辑处理
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                            <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                            content_type='text/xml', status=200)
    elif return_code == 'SUCCESS':
        # 拿到这次支付的订单号
        out_trade_no = xmlmsg['out_trade_no']
        print(xmlmsg)
        # 根据需要处理业务逻辑
        return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                            <return_msg><![CDATA[OK]]></return_msg></xml>""",
                            content_type='text/xml', status=200)



@check_header
def get_coupon(request):
    id = get_id_by_openid(request)
    list = get_coupon_db(id)

    #解析成传给前端的格式
    #字典生成器
    rdict = {index: value['state'] for index, value in enumerate(list)}

    re_json = {"succ": True, "msg": "操作成功", "data": rdict}

    return JsonResponse(re_json)


@check_header
def set_coupon_sta(request):
    id = get_id_by_openid(request)
    get_data = json.loads(request.body)

    #为配合前端接口修改格式，现在前端传入格式为
    # {
    #     'price': 0  ##0 、1、2
    #     'state': 1  ##1 、0  1-可以使用 0-不能使用 2-已经使用
    # }

    if get_data['price'] == 0:
        get_data['price'] = 'login'
    elif get_data['price'] == 1:
        get_data['price'] = 'share_once'
    elif get_data['price'] == 2:
        get_data['price'] = 'share_twice'


    update_coupon(id,get_data['price'],get_data['state'])
    re_json = {"succ": True, "msg": "操作成功", "data": {}}
    return JsonResponse(re_json)

@check_header
def get_all_goods(request):

    re_json = {"succ": True, "msg": "操作成功", "data": {'list' : get_all_goods_()}}
    return JsonResponse(re_json)


def get_class(request):

    #提供给小老板，单独的get
    if request.method == 'GET':

        phone_number = request.GET.get("phone_number",None)

        pwd = request.GET.get("pwd", None)

        #判断是否参数正确
        if pwd is None or phone_number is None:
            
            return render(request, 'index.html')

        get_data_by_1 = get_data_by_zhihuishu(phone_number, pwd)
        if get_data_by_1['succ'] == '1':
            re_json = {"succ": True, "msg": "操作成功", "data": {'list': get_data_by_1['data']}}
        else:
            re_json = {"succ": False, "msg": get_data_by_1['mess'], "data": {'list': get_data_by_1['data']}}

        return HttpResponse(json.dumps(re_json, ensure_ascii=False), content_type='application/json', charset='utf-8')

    #post请求，提供给小程序，取body中的字段的方法不一样
    elif request.method == 'POST':

        get_data = json.loads(request.body)
        type = get_data.get('type', None)

        phone_number = get_data['phone_number']
        pwd = get_data['pwd']

        if type == 1:
            get_data_by_1 = get_data_by_zhihuishu(phone_number,pwd)
            if get_data_by_1['succ'] == '1':
                re_json = {"succ": True, "msg": "操作成功", "data": {'list': get_data_by_1['data']}}
            else:
                re_json = {"succ": False, "msg": get_data_by_1['mess'], "data": {'list': get_data_by_1['data']}}

        return JsonResponse(re_json)


@check_header
def share_for_coupon(request):

    id = get_id_by_openid(request)

    if share_for_coupon_(id) :
        re_json = {"succ": True, "msg": "操作成功", "data": {}}
    else:
        re_json = {"succ": False, "msg": "所有优惠卷都已生效", "data": {}}

    return JsonResponse(re_json)

@check_header
def add_order(request):

    id = get_id_by_openid(request)

    get_data = json.loads(request.body)

    class_data_list = get_data['class_data_list']

    add_order_(id,get_data['price'],class_data_list)

    re_json = {"succ": True, "msg": "操作成功", "data": {}}

    return JsonResponse(re_json)

@check_header
def get_order_detail(request):

    id = get_id_by_openid(request)

    data = get_order(id)

    re_json = {"succ": True, "msg": "操作成功", "data": data}

    return JsonResponse(re_json)

def download_txt(request):

    get_order_bytxt()
    ###网上超的代码
    file_name = './txt/data.txt'

    def file_iterator(fn, chunk_size=512):
        while True:
            c = fn.read(chunk_size)
            if c:
                yield c
            else:
                break

    fn = open(file_name, 'rb')
    response_ = StreamingHttpResponse(file_iterator(fn))
    response_['Content-Type'] = 'application/octet-stream'
    response_['Content-Disposition'] = 'attachment;filename="data.txt"'

    return response_

def clear_txt(request):
    f = open('./txt/data.txt','w')
    f.close()
    return JsonResponse({"msg":"清除成功"})

def initialize_conpon(request):

    initialize_conpon_()

    return JsonResponse({"msg": "操作成功"})


def check_by_sid(request):

    # get_data = json.loads(request.body)
    sname = request.GET.get("sname", None)
    sid = request.GET.get("sid", None)
    pwd = request.GET.get("pwd", None)

    # 判断是否参数正确
    if pwd is None or sid is None or sname is None:

        return render(request,'index.html')
        #return HttpResponse("参数错误", content_type='application/json',charset='utf-8')
    else:

        get_data_ = check_by_Sid(str(sid), str(pwd), str(sname))

        if get_data_['succ'] == '1':

            re_json = {"succ": True, "msg": "操作成功", "data": {'list': get_data_['data']}}
        else:
            re_json = {"succ": False, "msg": get_data_['mess'], "data": {'list': get_data_['data']}}

        return HttpResponse(json.dumps(re_json,ensure_ascii=False), content_type='application/json', charset='utf-8')
