import time,functools

#异常
NOT_FOUND_UI="未找到对应ui控件"
def inforPrint(fux):
    functools.wraps(fux)
    def wrapper(self,*args,**kwargs):
        if 'infor' in kwargs:
            if kwargs['infor']!=None:
                print(self._UiAnazaed__deviceId+'：'+kwargs['infor'])
        if 'beforeTime' in kwargs:
            if kwargs['beforeTime']!=0:
                time.sleep(kwargs['beforeTime'])
        re=fux(self,*args,**kwargs)
        if 'endTime' in kwargs:
            if kwargs['endTime']!=0:
                time.sleep(kwargs['endTime'])
        return re
    return wrapper