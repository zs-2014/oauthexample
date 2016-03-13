#coding: utf-8
'''
为了测试方便，将client也写入到server中
只需要用户在浏览器中中输入http://host:12345/client/entrance
即可模拟整个过程，默认情况下模拟的是需要用户授权的过程，
如果仅仅只是为了获取access_token的话，那么可以在上述url
中增加查询字符串scope=snsapi_base便可直接获取
'''

import os, sys
import time
import json
import traceback
import urllib2
import urllib
import logging
import config
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine 
from tornado.gen import Return
from base import BaseHandler

log = logging.getLogger()

host = config.host
port = config.port
appid = config.appid
appsecret = config.appsecret
userid = config.userid 

class EntranceHandler(BaseHandler):
    def GET(self):
        params = self.input()
        scope = params.get('scope', 'snsapi_userinfo') or 'snsapi_userinfo'
        req_params = {'redirect_uri': 'http://%s:%s/client/auth_pass' % (host, port),
                       'scope': scope,
                       'response_type': 'code',
                       'appid': appid,
                       'userid': userid}
        self.redirect('http://%s:%s/oauth2/auth?%s' % (host, port, urllib.urlencode(req_params)))

    get = GET

class  AuthPassHandler(BaseHandler):

    @coroutine
    def GET(self):
        params = self.input()
        code = params.get('code')
        if not code:
            self.write('auth fails')
            raise Return('')

        req_params = {'code': code,
                      'appid': appid,
                      'userid': userid,
                      'secret': appsecret,
                      'grant_type': 'authorization_code'}
        url = 'http://%s:%s/oauth2/access_token?%s' % (host, port, urllib.urlencode(req_params))
        cli = AsyncHTTPClient()
        response = yield cli.fetch(url)
        rsp_dict = json.loads(response.body) 
        if rsp_dict['scope'] == 'snsapi_base':
            self.write(json.dumps(rsp_dict))
        else:
            req_params = {'access_token': rsp_dict['access_token'],
                          'openid': rsp_dict['openid'],
                          'lang': 'zh_CN'}
            url = 'http://%s:%s/oauth2/user_info?%s' % (host, config.port, urllib.urlencode(req_params))
            cli = AsyncHTTPClient()
            response = yield cli.fetch(url) 
            self.write(response.body)

    get = GET

