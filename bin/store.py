#coding: utf-8
import time

from util import Singleton

class Store(object):
    def __init__(self):
        pass

    def save_code_info(self, appid, userid, code, scope):
        '''将code保存起来
        '''
        raise NotImplementedError()

    def get_userinfo(self, userid):
        '''get user info by userid
        '''
        raise NotImplementedError()

    def get_appinfo(self, appid):
        '''get app info by appid
        '''
        raise NotImplementedError()
            
@Singleton
class SimpleStore(Store):
    def __init__(self):
        self.code_dict = {}
        self.token_dict = {}

    #默认300秒过期
    #redirect_uri是否应该有长度限制呢？
    def save_code_info(self, appid, userid, code, scope, redirect_uri):
        self.code_dict[code] = {'appid': appid,
                                'userid': userid,
                                'redirect_uri': redirect_uri,
                                'code': code,
                                'scope': scope,
                                'expires': int(time.time())+ 300}
        return True

    def get_code_info(self, code):
        return self.code_dict.get(code)

    def save_token_info(self, token, appid, userid, scope):
        self.token_dict[token] = {'appid': appid,
                                  'userid': userid,
                                  'scope': scope,
                                  'token': token,
                                  'expires': int(time.time())+7200}
    def get_token_info(self, token):
        return self.token_dict.get(token)
    
    def get_userinfo(self, userid):
        return {'userid': userid,
                'nickname': 'test',
                'city': '北京',
                'country': "中国",
                'headimgurl': ('http://wx.qlogo.cn/mmopen/g3MonUZtNH'
                              'kdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYV'
                              'Y0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv'
                              '84eavHiaiceqxibJxCfHe/46'),
                } 

    def get_appinfo(self, appid):
        return {'appid': appid,
                'appsecret': 'test',
                'oauth_domain': '*',
                'is_disabled': False} 

    

@Singleton
class Validator(object):
    '''对数据进行校验
    '''
    def __init__(self, store):
        self.store = store 
    
    def appid_is_valid(self, appid):
        ''' 检查该公众号是否存在
        '''
        app_info = self.store.get_appinfo(appid) 
        return bool(app_info)

    def userid_is_valid(self, userid):
        ''' 检查该用户是否存在
        '''
        user_info = self.store.get_userinfo(userid)
        return bool(user_info) 

    def check_appsecret(self, appid, appsecret):
        '''校验appid对应的appsecret是否对
        '''
        app_info = self.store.get_appinfo(appid)
        #检查app_secret
        #这里简单返回True
        return True 

    def check_appid_domain(self, appid, domain):
        ''' 检查appid所配置的授权域名
            是否和这个域名相符合
        '''
        app_info = self.store.get_appinfo(appid)
        return True 

    def check_code(self, code, appid):
        '''检查code合不合法
        '''
        code_info = self.store.get_code_info(code)
        if not code_info or code_info['expires'] < int(time.time()):
            #对待过期这个可以做一次删除操作
            return False
        return code_info['appid'] == appid
        

simple_store = SimpleStore()
validator = Validator(simple_store)


