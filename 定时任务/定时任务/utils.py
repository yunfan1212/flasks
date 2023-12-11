import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
def job1(f):
    print( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), f)

def job2(args1, args2, f):
    print (f, args1, args2)

def job3(**args):
    print( args)

def start(psm,env,tag,seconds,id,minute,chat_id):
    print(11111111111111)