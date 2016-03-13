#coding: utf-8
'''
    这里定义了一些常量
'''

#响应类型
response_types = ('code', )

#授权作用域
scopes = (snsapi_base, snsapi_userinfo) = ('snsapi_base', 'snsapi_userinfo')

#请求access_token时grant_type的值
grant_types = (auth_code, ) = ('authorization_code', )
