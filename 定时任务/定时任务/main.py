
'''
from flask import Flask
from 定时任务 import task

# 创建app
app = Flask(__name__)# 注册蓝图
app.register_blueprint(task.Taskapi)

if __name__ == '__main__':
    scheduler = task.init()
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host="0.0.0.0", port=6000)
'''
#hello