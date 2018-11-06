#多线程操作模块
import threading

#要执行的设备List、需要执行的方法、方法的参数
def startThrading(deviceList,func):
    for i in deviceList:
        threading.Thread(target=func,args=(i,)).start()