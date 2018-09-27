# miniprogram config file
from string import Template

APPID = 'wxade43df560e74b6c'

APPSECRET = '4e62b8f7d726f5340c9d8137a20d243d'

Mch_id = ""
Mch_key = ""

_CODE2SESSION = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={APPSECRET}&js_code=$CODE&grant_type=authorization_code'

# get your code api url like this:
# my_url = CODE2SESSION.substitute({'CODE':'123'})
CODE2SESSION = Template(_CODE2SESSION)

Order_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
