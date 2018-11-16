#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'pi'
__email__ = 'pipisorry@126.com'

"""
import http.cookiejar
import requests
import json
import time
from lxml import etree




LOGIN_URL = 'https://passport.zhihuishu.com/login'
url1="https://passport.zhihuishu.com/login?service=http://online.zhihuishu.com/onlineSchool/"


user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive' ,'Host' : 'passport.zhihuishu.com' ,'Referer' : 'https://passport.zhihuishu.com/login?service=http://online.zhihuishu.com/onlineSchool/'}




# for item in cookie:
#     print('Name = ' + item.name)
#     print('Value = ' + item.value)

#r=requests.post("http://online.zhihuishu.com/onlineSchool/json/student/loadStuCourseRecruit", data=data1,cookies = cookie3,headers =headers )
#a = r.json()
#print(json.dumps(a,indent=4))

def get_return_dict(succ,mess,data):
    dict= {}
    dict['succ'] = succ
    dict['mess'] = mess
    dict['data'] = data
    return dict

def get_data_by_zhihuishu(username,password):

    session = requests.session()
    try:
        r = session.get(url1,timeout =10)
        r.raise_for_status()
    except:

        return get_return_dict('-1', '网络异常请重试', '')
    html = r.text
    selector = etree.HTML(html)
    lt = selector.xpath("//input[@name='lt']/@value")[0]
    execution = selector.xpath("//input[@name='execution']/@value")[0]
    _eventId = selector.xpath("//input[@name='_eventId']/@value")[0]

    values = {
        'lt': lt,
        'execution': execution,
        '_eventId': _eventId,
        'username': username,
        'password': password,
        'clCode': '',
        'clPassword': '',
        'tlCode': '',
        'tlPassword': ''
    }
    try:
        session.post(LOGIN_URL, data=values).raise_for_status()
    except:
        return get_return_dict('-1', '网络异常请重试', '')


    cookiedict = requests.utils.dict_from_cookiejar(session.cookies)
    if 'CASLOGC' not in cookiedict.keys():
        return get_return_dict('-1','账号或者密码错误','')

    #print(cookiedict)
    data1 = {
        "loadType": 0
    }
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    try:
        r = session.post("http://online.zhihuishu.com/onlineSchool/json/student/loadStuCourseRecruit", data=data1,
                         headers=headers)
        r.raise_for_status()
    except:
        return get_return_dict('-1', '网络异常请重试', '')
    a = r.json()
    #print(a)
    list_data=[]
    for b in a["maps"]:
        dict= {}
        dict['courseName'] = b['courseName']
        dict['planProgress'] = b['actualProgress']
        list_data.append(dict)
    return get_return_dict('1','查询成功',list_data)

#根据学号进行查询
def check_by_Sid(sid,password,name):

    session = requests.session()
    try:
        r = session.get(url1, timeout=30)
        r.raise_for_status()
    except:

        return get_return_dict('-1', '网络异常请重试', '')

    url_school_list  = "https://passport.zhihuishu.com/user/getAllSchool?date=Tue%20Nov%2013%202018%2014:20:13%20GMT+0800%20(%E5%8F%B0%E5%8C%97%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"


    try:
        #获得所有的学校列表
        r = session.post(url_school_list, timeout=30)
        r.raise_for_status()
    except:

        return get_return_dict('-1', '网络异常请重试', '')

    #从接口中拿到所有的学校ID
    list_schoohID = r.json()['listSchool']

    name_list = [x['name'] for x in list_schoohID]

    #从名字列表中，根据name 得到index ---然后找到ID
    try:
        school_id = list_schoohID[name_list.index(name)]['schoolId']
    except:
        return get_return_dict('-1', '没有找到对应的学校', '')


    url_for_login = "https://passport.zhihuishu.com/user/validateCodeAndPassword"

    value ={
        'code' : sid,
        'password' : password,
        'schoolId': str(school_id),
        'captcha' : ''
    }

    r_total = session.post(url_for_login,data=value,headers=headers)
    try:
        url_for_cookie ="https://passport.zhihuishu.com/login?pwd="+r_total.json()['pwd']+"&service=http://online.zhihuishu.com/onlineSchool/"
    except:
        return get_return_dict('-1', '账号或者密码错误', '')

    session.headers[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

    res = session.get(url_for_cookie)

    cookiedict = requests.utils.dict_from_cookiejar(session.cookies)
    #再次判断是否登录成功

    if 'CASLOGC' not in cookiedict.keys():
        return get_return_dict('-1','账号或者密码错误','')
    else:
        data1 = {
            "loadType": 0
        }
        headers_cookie = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
        session.headers=headers_cookie

        try:
            print(session.headers)
            r = session.post("http://online.zhihuishu.com/onlineSchool/json/student/loadStuCourseRecruit", data=data1,
                             )

            r.raise_for_status()
        except:
            print('==================')
            return get_return_dict('-1', '网络异常请重试', '')
        a = r.json()

        list_data = []
        for b in a["maps"]:
            dict = {}
            dict['courseName'] = b['courseName']
            dict['planProgress'] = b['actualProgress']
            list_data.append(dict)
        return get_return_dict('1', '查询成功', list_data)

def run():
    print(check_by_Sid('1710044209','123456a','咸阳师范学院'))
