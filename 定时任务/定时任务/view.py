from 定时任务 import app
from 定时任务.task import Taskapi

app.register_blueprint(Taskapi)