#coding: utf-8
import os, sys
import hashlib
import types
import uuid

unicode_to_utf8 = lambda t: t.encode('utf-8') if isinstance(t, types.UnicodeType) else str(t)

#单例模式装饰器
def Singleton(cls):
    ins_map = {}
    def _(*args, **kwargs):
        if cls not in ins_map:
            ins_map[cls] = cls(*args, **kwargs) 
        return ins_map[cls]
    return _ 

#生成重定向时带的code
def gen_code(appid, userid):
    return uuid.uuid4().hex

#生成accesss_token
#获取会用到某种算法生成
def gen_access_token(appid):
    return uuid.uuid4().hex 

#简单的算法生成openid
def gen_openid(appid, userid):
    md5 = hashlib.md5()
    md5.update(appid+userid)
    return md5.hexdigest()
    
