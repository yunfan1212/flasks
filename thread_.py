import threading
from threading import Thread

class MyThread(Thread):
    def __init__(self,func,args):
        super(MyThread,self).__init__()
        self.func=func
        self.args=args
        self._pauseFlag=threading.Event()    #暂停标志位
        self._pauseFlag.set()

    def run(self):
        self._pauseFlag.wait()    #当标志位为false 则放行，否则阻塞
        if len(self.args)>0:
            self.result=self.func(self.args)
        else:
            self.result=self.func()

    def pause(self):
        self._pauseFlag.clear()

    def restart(self):
        self._pauseFlag.set()

    def get_result(self):
        try:
            return self.result
        except:
            return None