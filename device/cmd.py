import os
#执行cmd,返回的信息包含sucess即成功
def mkCmdByPope(cmd,*args,sucess=None):
    if(args!=None):
        cmd=cmd % args
    resault=os.popen(cmd)
    resault=resault.read()
    if sucess!=None:
        resault=resault.strip()
        if "not found" in resault:
            raise BaseException('此设备已断开连接，无需继续操作')
        if sucess in resault:
            return True
        else:
            return False
    else:
        return True

#此执行方式，只要有结果返回即为执行成功
def mkCmdByPopeReturnFalseTrue(cmd,*args):
    if(args!=None):
        cmd=cmd % args
    resault =os.popen(cmd)
    resault=resault.read()
    if resault:
        if "not found" in resault:
            raise BaseException('此设备已断开连接，无需继续操作')
        return True
    else:
        return False

#返回控制台信息
def mkCmdReturnInfor(cmd,*args):
    if (args != None):
        cmd = cmd % args
    resault = os.popen(cmd)
    resault = resault.read()
    if resault:
        if "not found" in resault:
            raise BaseException('此设备已断开连接，无需继续操作')
        return str(resault).strip()
    else:
        return None


