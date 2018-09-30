from weixin.login_interface.login_operation import *


def run():
    openid = "wwwwwwwwww"
    header = generate_header_value(openid)
    write_login_header(openid,header)