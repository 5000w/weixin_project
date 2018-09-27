from utils.redis_utils import write_to_redis, del_from_redis, read_from_redis, prolong_redis_key
import time
from django.http import JsonResponse
from string import Template
import json
_OPENID_KEY = f'user_$openid'

TEMPLATE_OPENID_KEY = Template(_OPENID_KEY)

LIVE_TIME = 5 * 60



def check_header(func):
    def _func(request):
        request_data = json.loads(request.body)
        openid = request_data["openid"]  #获取前端的openid
        request_header = request_data["header"]
        redis_header = get_header_from_redis(openid)
        if request_header != redis_header:
            rsp = {"succ": False, "data": {}, "msg": "header 验证失败"}
            return JsonResponse(rsp)
        func(request)

    return _func


def generate_header_value(openid):
    return {"time": int(time.time()), "openid": openid}


def write_login_header(openid, header_info):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return True if write_to_redis(key, header_info, ex=LIVE_TIME) else False


def del_login_header(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return True if del_from_redis(key) else False


def get_header_from_redis(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return read_from_redis(key)


def update_login_header_time(openid):
    key = TEMPLATE_OPENID_KEY.substitute({"openid": openid})
    return True if prolong_redis_key(key, LIVE_TIME) else False
