#coding=utf-8
'''模型启动文件 jyf'''
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from 定时任务 import app
from 定时任务 import avic_info
from config import Config
#################################

print(__name__)
if __name__ == '__main__':
    '''蓝图下的定时器'''
    app.config.from_object(Config())
    scheduler = avic_info.init()
    scheduler.init_app(app=app)
    scheduler.start()
    port=8011
    http_server=WSGIServer(("0.0.0.0",int(port)),app)
    http_server.serve_forever()