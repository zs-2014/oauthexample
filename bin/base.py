#coding: utf-8
'''
    BaseHandler，所有的WebHandler都继承自这个类
'''

from tornado.web import RequestHandler
import logging
import traceback
import urllib
import time
import util

log = logging.getLogger()

class BaseHandler(RequestHandler):
    def initialize(self):
        self.params = None
        #self.set_header('Content-Type', 'application/json; charset=UTF-8')    

    def prepare(self):
        self.create_tm = time.time()

    #|status|method|path|create_time|diff_time1|diff_time2|query_string|input_argument|output
    def finish(self, *args, **kwargs):
        finsh_tm1 = time.time()
        rtn_content = b''.join(self._write_buffer)
        try:
            super(BaseHandler, self).finish(*args, **kwargs)
        except Exception, e:
            log.warn(traceback.format_exc())
        msg = [] 
        finsh_tm2 = time.time()
        diff_tm1 = int((finsh_tm1-self.create_tm)*1000000)
        diff_tm2 = int((finsh_tm2-self.create_tm)*1000000)
        msg.append('%d' % self.get_status())
        msg.append(util.unicode_to_utf8(self.request.method))
        msg.append(util.unicode_to_utf8(self.request.path or '/'))
        msg.append('%d' % int(self.create_tm))
        msg.append('%d' % diff_tm1)
        msg.append('%d' % diff_tm2)
        msg.append(urllib.unquote_plus(util.unicode_to_utf8(self.request.query)))
        msg.append(str(self.request.arguments))
        msg.append(rtn_content)
        log.info('|'.join(msg))

    def input(self, strip=True):
        if self.params is not None:
            return self.params
        self.params = {}
        for k, v in self.request.arguments.iteritems():
            self.params[util.unicode_to_utf8(k)] = util.unicode_to_utf8(strip and v[-1].strip() or v[-1])
        return self.params
