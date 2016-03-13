#coding: utf-8
'''
OAuth所需要的所有的handler
''' 
import os, sys
import time
import traceback
import logging
import urlparse
import constants
from base import BaseHandler
from response import RET, error, success
from store import simple_store, validator
from tornado.gen import coroutine 
import util

log = logging.getLogger()

class OAuthHandler(BaseHandler):
    '''
        授权请求处理
        1.如果scope为snsapi_base,则不需要用户同意，静默跳转到redirect_uri并带上code
        2.如果scop为snsapi_userinfo,这个需要用户授权同意，
          用户同意之后，跳转到redirect_uri上并且带上code
    '''

    @coroutine
    def GET(self):
        #参数完全可以写个通用的参数校验器
        try:
            params = self.input() 
            appid = params['appid']
            userid = params['userid']
            scope = params['scope']
            rsp_type = params['response_type']
            redirect_uri = params['redirect_uri']
        except Exception, e:
            log.warn(traceback.format_exc())
            return

        if scope not in constants.scopes or rsp_type not in constants.response_types:  
            return

        if not validator.appid_is_valid(appid) or not validator.userid_is_valid(userid):
            return

        url_ret = urlparse.urlsplit(redirect_uri)
        #没有跳转域名或者跳转域名不合法
        if not url_ret.netloc or not validator.check_appid_domain(appid, url_ret.netloc):
            return
        code = util.gen_code(appid, userid) 
        simple_store.save_code_info(appid, userid, code, scope, redirect_uri)
        #不需要用户确认授权
        if scope == constants.snsapi_base:
            self.redirect('%s?code=%s' % (redirect_uri, code))
        #需要用户授权
        elif scope == constants.snsapi_userinfo:
            self.render('oauth.html', code=code)

    get = GET

class UserAuthPassHandler(BaseHandler):
    '''
        用户点击同意授权所请求的uri，然后跳转到授权请求中redirect_uri所指向的url
        并且带上code
    '''
    @coroutine
    def GET(self):
        try:
            params = self.input()
            code = params['code']
        except Exception, e:
            log.warn(traceback.format_exc())
            return self.write(error(RET.SOME_ERROR))
        if not code:
            return self.write(error(RET.SOME_ERROR))
        code_info = simple_store.get_code_info(code)
        if not code_info or code_info['expires'] <= int(time.time()):
            return self.write(error(RET.SOME_ERROR))

        #不考虑用户授权不通过，区别仅仅只是code有无得问题
        self.redirect('%s?code=%s' % (code_info['redirect_uri'], code))

    get = GET
            
class AccessTokenHandler(BaseHandler):
    @coroutine
    def GET(self):
        try:
            params = self.input()
            code = params['code']
            appid = params['appid']
            secret = params['secret']
            grant_type = params['grant_type']
        except Exception, e:
            log.warn(traceback.format_exc())
            return self.write(error(RET.SOME_ERROR))

        if not all([code, appid, secret, grant_type in constants.grant_types]):
            return self.write(error(RET.SOME_ERROR))
        if not validator.check_code(code, appid):
            return self.write(error(RET.SOME_ERROR))
        if not validator.check_appsecret(appid, secret):
            return self.write(error(RET.SOME_ERROR))
        code_info = simple_store.get_code_info(code)
        acc_token = util.gen_access_token(appid)
        simple_store.save_token_info(acc_token, code_info['appid'], code_info['userid'], code_info['scope'])
        openid = util.gen_openid(appid, code_info['userid'])
        return self.write(success({'expires_in': 7200,
                                   'openid': openid,
                                   'scope': code_info['scope'],
                                   'access_token': acc_token}))
    get = GET


class UserinfoObtainHandler(BaseHandler):

    @coroutine
    def GET(self):
        try:
            params = self.input()
            access_token = params['access_token']
            openid = params['openid']
            lang = params['lang']
        except Exception, e:
            log.warn(traceback.format_exc())
            return self.write(error(RET.SOME_ERROR))
        if not all([access_token, openid, lang]):
            return self.write(error(RET.SOME_ERROR)) 

        token_info = simple_store.get_token_info(access_token)  

        #不存在或者过期了
        if not token_info or token_info['expires'] < int(time.time()):
            return self.write(error(RET.SOME_ERROR))
        if token_info['scope'] != constants.snsapi_userinfo:
            return self.write(error(RET.SOME_ERROR))

        #相同的算法生成出来的openid应该是一致的
        if openid != util.gen_openid(token_info['appid'], token_info['userid']):
            return self.write(error(RET.SOME_ERROR))
        user_info = simple_store.get_userinfo(token_info['userid'])
        #对userinfo的一些处理可以放在这里
        self.write(success(user_info))

    get = GET
