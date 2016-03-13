#coding: utf-8
'''
    错误代码
    为了简便起见，只写了成功失败两种简单的情况
    实际上分类更细一些，比如参数错误，code不合法
    之类的错误
'''

import json

#错误代码
class RET(object):
    OK =  0
    SOME_ERROR = 40029

#错误代码描述
error_map = {
    RET.OK : "ok",
    RET.SOME_ERROR : "出错了",
}

def  error(err_code, respmsg=""):
    return json.dumps({'errcode': err_code, 'errmsg': respmsg or error_map.get(err_code, '系统错误')})

def success(data):
    return json.dumps(data)
