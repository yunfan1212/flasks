


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:job_1',    #方法名   app为文件路径
            'args': (10, 20),
            'trigger': 'cron',    #定时调度，负责调度方式
            'hour': 17,
            'minute': 1
        },
        {
            'id': 'job2',
            'func': 'app:job_1',
            'args': (3, 4),
            'trigger': 'interval',    #间隔调度
            'seconds': 5
        }
    ]