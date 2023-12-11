#coding=utf8
print("模型开始启动")
from flask import Flask,request
from gevent.pywsgi import WSGIServer
import json
import traceback
import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(filename)s-%(levelname)s-%(lineno)d-%(message)s")
from mysql_.mapping_task import get_task_md_ids,update_tech_task,get_status
import datetime
from new_tech_finding.model_infer import NewTechFinding
from utils.my_thread import MyThread
import gc
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from config import args
from mysql_.mapping_task import get_task_by_state
from language_classify.lang_main import trigger_task
app=Flask(__name__)
new_tech_model=NewTechFinding()
app.config.from_object(args())
scheduler = APScheduler(BackgroundScheduler(timezone='Asia/Shanghai'))

from keywords_finding.keyword_extract import KeyWordExtract



import time
def model_fn(taskId):
    res = {"code": 201, "msg": "请检查输入数据，数据为空"}
    id =taskId
    logging.info("输入信息 taskId:{}".format(id))
    try:
        ids = get_task_md_ids(id)
        logging.info("输入信息 {}".format(ids))
        if len(ids) > 0:
            update_tech_task(id, status=2)  # 开始执行
            '''模型识别'''
            result,res1 = new_tech_model.forward(ids=ids)
            if len(result) == 0 and res1=="无关键词":
                cur_time = datetime.datetime.now()
                update_tech_task(id, endTime=cur_time, status=4)  # 未识别到新数据
                res["msg"] = "成功"
            elif len(result) == 0 and res1=="无相关数据":
                cur_time = datetime.datetime.now()
                update_tech_task(id, endTime=cur_time, status=6)  # 无数据
            elif len(result) > 0:
                # 插入数据
                new_tech_model.insert_result(taskId=id, result=result)
                cur_time = datetime.datetime.now()
                update_tech_task(id, endTime=cur_time, status=3)  # 已经执行
                res["msg"] = "成功"
            res["code"] = 200
    except:
        traceback.print_exc()
        res["msg"] = str(traceback.print_exc())
        logging.info(traceback.print_exc())
        cur_time = datetime.datetime.now()
        update_tech_task(id, endTime=cur_time, status=5)  # 已经执行
    return res

'''加载执行中的任务'''
task=get_task_by_state()
num=0
task_thread=dict()
def job_summary():
    global num
    global task
    global task_thread
    task1 = get_task_by_state()
    logging.info("获取任务{}".format(task1))
    if num<=5 and (len(task)>0 or len(task1)>0):
        if len(task)==0 and len(task1)>0:
            task=task1
        task_id=task.pop(0)
        num+=1
        try:
            t=MyThread(model_fn,args=task_id)
            t.start()
            task_thread[task_id]=t
            t.join()
            del task_thread[task_id]
            del t
            res=gc.collect()
            logging.info("清空对象:{}".format(res))
        except:
            traceback.print_exc()
            logging.info(traceback.print_exc())
        finally:
            num-=1
    else:
        '''将数据列为候选名单'''
        for id in task:
            update_tech_task(id, status=7)
    return "done"



def job_keywords():
    try:
        logging.info("开始进行关键词抽取")
        m = KeyWordExtract()
        m.forward()
        t=MyThread(m.forward,args=())
        t.start()
        t.join()
        del t
        res=gc.collect()
        logging.info("清空对象:{}".format(res))
    except:
        traceback.print_exc()
        logging.info(traceback.print_exc())
    return "done"





@app.route("/test",methods=["POST","GET"])
def test():
    return "成功"


@app.route("/12yuan/langClassify",methods=["POST","GET"])
def langClassify():
    trigger_task()
    res = {"code": 200, "msg": "后台开始执行"}
    return json.dumps(res,ensure_ascii=False)



@app.route("/12yuan/newTechPause",methods=["POST","GET"])
def newTechPause():
    res={"code":200,"msg":"已暂停"}
    id=request.form.get("taskId")
    if id in task_thread:
        task_thread[id].pause()
    logging.info("输入信息 taskId:{}".format(id))
    return json.dumps(res,ensure_ascii=False)


@app.route("/12yuan/newTechRemuse", methods=["POST", "GET"])
def newTechRemuse():
    res = {"code": 200, "msg": "已执行"}
    id = request.form.get("taskId")
    if id in task_thread:
        task_thread[id].restart()
    logging.info("输入信息 taskId:{}".format(id))
    return json.dumps(res, ensure_ascii=False)



type={0:"已删除", 1:"未执行",2:"正在执行中",3:"已执行", 4:"未识别到新技术",5:"服务异常",6:"无数据",7:"已经加入列表"}
@app.route("/12yuan/newTechFinding",methods=["POST","GET"])
def newTechFinding():
    res={"code":200,"msg":"已加入任务列表"}
    id=request.form.get("taskId")
    #加入到待执行列表中
    status=get_status(id)
    if status==1:
        update_tech_task(id,7)
        task.append(id)
    else:
        res["msg"]=type[status]
    logging.info("输入信息 taskId:{}".format(id))
    return json.dumps(res,ensure_ascii=False)



if __name__ == '__main__':
    #部署之前先进行数据处理   dataprepare.py
    print("模型启动完成。")
    scheduler.add_job(func=job_summary, id="new_tech_finding", args=(), trigger='interval', seconds=2,
                      replace_existing=True)
    # scheduler.add_job(func=job_keywords, id="keywords_extract", args=(), trigger='cron',hour=3,
    #                   replace_existing=True)

    scheduler.init_app(app=app)
    scheduler.start()
    http_server=WSGIServer(('0.0.0.0',int(8012)),app)
    http_server.serve_forever()


