# miniprogram config file
from string import Template

APPID = 'wxa1d355f769c6075b'

APPSECRET = 'a490035bf5db169434c881c84c7126d1'

Mch_id = ""
Mch_key = ""

_CODE2SESSION = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={APPSECRET}&js_code=$CODE&grant_type=authorization_code'

# get your code api url like this:
# my_url = CODE2SESSION.substitute({'CODE':'123'})
CODE2SESSION = Template(_CODE2SESSION)

Order_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
