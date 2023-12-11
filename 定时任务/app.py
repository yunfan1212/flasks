#coding=utf-8


from flask_apscheduler import APScheduler
from flask import Flask


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job_1',    #方法名
            'args': (10, 20),
            'trigger': 'cron',    #定时调度，负责调度方式
            'hour': 17,
            'minute': 1
        },
        {
            'id': 'job2',
            'func': '__main__:job_1',
            'args': (3, 4),
            'trigger': 'interval',    #间隔调度
            'seconds':2
        }
    ]


def job_1(a, b):  # 一个函数，用来做定时任务的任务。
    print(str(a) + ' ' + str(b))


app = Flask(__name__)  # 实例化flask
app.config.from_object(Config())  # 为实例化的flask引入配置


@app.route('/',methods=["POST","GET"])  # 首页路由,没有methods报405错误
def hello_world():
    return 'hello'


if __name__ == '__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run(debug=True)  # 启动flask


