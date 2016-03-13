#coding: utf-8
import os, sys
import tornado.httpserver as httpserver
import tornado.web as web
import tornado.ioloop as ioloop

bin_path = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(bin_path, 'templates')
sys.path.append(os.path.join(os.path.dirname(bin_path), 'conf'))

import config
import urls
from logger import init_logger

log = init_logger(config.logfile)


if __name__ == '__main__':

    app = web.Application(handlers=urls.urls,
                          template_path=template_path)
    server = httpserver.HTTPServer(app)
    server.listen(config.port)
    log.info("server start at %s", config.port)
    ioloop.IOLoop.instance().start()
