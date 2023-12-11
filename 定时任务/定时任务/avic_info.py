#coding=utf-8

from flask import Blueprint
__name__=="app"            #与config的名字一致
avic_info=Blueprint("avic",__name__)


from flask_apscheduler import APScheduler
from flask import Flask

Scheduler = None
taskdict = {}

def init():
    global Scheduler
    Scheduler = APScheduler()
    return Scheduler



def job_1(a, b):  # 一个函数，用来做定时任务的任务。
    print(str(a) + ' ' + str(b))






