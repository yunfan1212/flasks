

import psutil
import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')




def mem_total():
    mem=psutil.virtual_memory()
    zj=float(mem.total)
    ysy=float(mem.used)
    kx=float(mem.free)
    logging.info('系统总计内存:%d.3GB' % zj)
    logging.info('系统已经使用内存:%d.3GB' % ysy)
    logging.info('系统空闲内存:%d.3GB' % kx)
    logging.info('========================================')
    return

