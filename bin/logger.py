#coding: utf-8
#一个简单的log初始化函数

import os, sys
import logging
import types
from logging.handlers import WatchedFileHandler

def add_handler(log, file_nm, lvl):
    msg_format = '%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
    if file_nm.lower() == 'stdout':
        hdr = logging.StreamHandler(sys.stdout)
    else:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_nm))) 
        except OSError, e:
            #已经存在
            if e.args[0] != 17:
                raise
        hdr = WatchedFileHandler(file_nm)
    hdr.setLevel(lvl)
    hdr.setFormatter(logging.Formatter(msg_format))
    log.addHandler(hdr)
    
def init_logger(conf, logger_name=None):
    '''
        {'INFO': '../log/info.log',
         'WARN': '../log/warn.log'}
         or single filepath and level is debug
    '''
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)

    if isinstance(conf, types.DictType):
        for lvl_nm, file_nm in conf.iteritems():
            add_handler(log, file_nm, lvl_nm.upper())
    else:
        add_handler(log, conf, logging.DEBUG) 
    return log

if __name__ == '__main__':
    def test_single_file_conf():
        log = init_logger('stdout') 
        log.debug('level debug msg')
        log.info('level info msg')
        log.warn('level warn msg')
        log.error('level error msg')

    test_single_file_conf()
    def test_dict_conf():
        conf = {'INFO': '../log/info.log',
                'DEBUG': '../log/debug.log',
                'warn': '../log/warn.log'}
        log = init_logger(conf)
        log.debug("level debug msg")
        log.info('level info msg')
        log.warn('level warn msg')
    test_dict_conf()
