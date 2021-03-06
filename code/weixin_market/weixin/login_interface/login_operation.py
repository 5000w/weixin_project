from utils.redis_utils import write_to_redis, del_from_redis, read_from_redis, prolong_redis_key, write_to_redis_hash, read_from_redis_hash
import time
from django.http import JsonResponse
from string import Template
from weixin.models import Weixin_user
import json
_OPENID_KEY = f'user_$openid'

TEMPLATE_OPENID_KEY = Template(_OPENID_KEY)

LIVE_TIME = 5 * 60 * 60 * 60 * 60



def check_header(func):
    def _func(request):
        header = request.META
        openid = header["HTTP_OPENID"]  #获取前端的openid
        time = header["HTTP_TIME"]
        redis_header = get_header_from_redis(openid)
        try:
            print(f'{redis_header["openid"]} \n {redis_header["time"]} \n {openid} \n {time}')
            if redis_header["openid"] != openid or str(redis_header["time"]) != time:
                rsp = {"succ": False, "data": {}, "msg": "header 验证失败"}
                return JsonResponse(rsp)
        except KeyError:
            rsp = {"succ": False, "data": {}, "msg": "header 验证失败"}
            return JsonResponse(rsp)
        return func(request)
    return _func


def get_id_by_openid(request):
    header = request.META
    openid = header["HTTP_OPENID"]
    #openid = "onAnm5UnBKJ9X-1738uWpA2cJPdI" #张雨生调试接口
    user = Weixin_user.objects.get(openid=openid)
    return user.id

def generate_header_value(openid):
    return {"time": int(time.time()), "openid": openid}


def write_login_header(openid, header_info):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    result = write_to_redis_hash(key, header_info)
    if result:
        update_login_header_time(openid)
        return True
    return False


def del_login_header(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return True if del_from_redis(key) else False


def get_header_from_redis(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return read_from_redis_hash(key)


def update_login_header_time(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return True if prolong_redis_key(key, LIVE_TIME) else False
