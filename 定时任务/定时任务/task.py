import uuid
import 定时任务.utils as utils
from flask_apscheduler import APScheduler
from flask import Blueprint, jsonify, request



Taskapi = Blueprint("task", __name__, url_prefix="/task")
Scheduler = None
taskdict = {}

def init():
    global Scheduler
    Scheduler = APScheduler()
    return Scheduler


# 暂停任务
# http://127.0.0.1:5000/task/pause?id=2
@Taskapi.route('/pause', methods=['GET'])
def pause_job():
    job_id = request.args.get('id')
    Scheduler.pause_job(str(job_id))
    response = {}
    response["msg"] = "success"
    return jsonify(response)


# 恢复任务
# http://127.0.0.1:5000/task/resume?id=2
@Taskapi.route('/resume', methods=['GET'])
def resume_job():
    job_id = request.args.get('id')
    Scheduler.resume_job(str(job_id))
    response = {}
    response["msg"] = "success"
    return jsonify(response)


# 获取任务
# http://127.0.0.1:5000/task/getjobs
@Taskapi.route('/getjobs', methods=['GET'])
def get_task():
    # jobs = Scheduler.get_jobs()
    # print(str(pickle.dumps(jobs)))
    return jsonify(taskdict)


# 移除任务
@Taskapi.route('/removejob', methods=['GET'])
def remove_job():
    job_id = request.args.get('id')
    Scheduler.remove_job(str(job_id))
    response = {}
    response["msg"] = "success"
    return jsonify(response)



# 添加任务
# http://cab912dac880.ngrok.io/task/addjob?tasktype=interval&minute=10&psm=caijing.charge.union_service&tag=prod&env=product&chat_id=6911623998451269634
@Taskapi.route('/addjob', methods=['GET'])
def add_task():
    global taskdict
    psm = request.args.get('psm', "cmp.ecom.settle")
    tag = request.args.get('tag', "prod")
    env = request.args.get('env', "boe")
    chat_id = request.args.get('chat_id', "6911623998451269634")
    tasktype = request.args.get('tasktype', "interval")
    minute = request.args.get('minute', "10")
    minute = float(minute)
    response = {}
    response["msg"] = "success"
    seconds = minute * 60

    # trigger='interval' 表示是一个循环任务，每隔多久执行一次
    if tasktype == "interval":
        id = str(uuid.uuid4())
        response["taskid"] = id
        response["data"] = [psm,env,tag,str(seconds)+"秒"]
        taskdict[id] = response["data"]
        #添加一个任务，并指定间隔进行触发

        Scheduler.add_job(func=utils.start, id=id, args=(psm,env,tag,seconds,id,minute,chat_id), trigger='interval', seconds=seconds,
                          replace_existing=True)
    else:
        response["id"] = ""
        response["msg"] = "tasktype 类型不存在"

    return jsonify(response)