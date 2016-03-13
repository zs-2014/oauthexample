#coding: utf-8

from handler import (OAuthHandler, UserAuthPassHandler, AccessTokenHandler, UserinfoObtainHandler)

#模拟客户端请求的url
from client import EntranceHandler, AuthPassHandler

urls = [('/oauth2/auth', OAuthHandler), #请求oauth认证的
        ('/oauth2/access_token', AccessTokenHandler), #获取access_token
        ('/oauth2/user_info', UserinfoObtainHandler), #拉取用户基本信息
        ('/oauth2/pass', UserAuthPassHandler), #用户点击授权成功

        #模拟客户端
        ('/client/entrance', EntranceHandler), #模拟客户端url
        ('/client/auth_pass', AuthPassHandler), #用户点击授权成功
        ]
