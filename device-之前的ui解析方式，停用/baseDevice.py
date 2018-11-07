from device.cmd import *
import os
from io import StringIO
#获取当前连接设备的List
import time
#raise：当未有设备连接，将抛出一个错误
def inforPrint(fux):
    def wrapper(*args,**kwargs):
        if 'infor' in kwargs:
            if kwargs['infor']!=None:
                print(args[0]+"："+kwargs['infor'])
        if 'beforeTime' in kwargs:
            if kwargs['beforeTime']!=0:
                time.sleep(kwargs['beforeTime'])
        temp=fux(*args,**kwargs)
        if 'endTime' in kwargs:
            if kwargs['endTime']!=0:
                time.sleep(kwargs['endTime'])
        return temp
    return wrapper
def getNowConnectDevice():
    str = os.popen('adb devices')
    str = str.read()
    f = StringIO(str)
    deviceList = []
    while True:
        s = f.readline()
        if s == '':
            break
        s = s.split()
        if s != [] and s[0] !='List':
            deviceList.append(s[0])
    if deviceList==[]:
        raise BaseException("当前未有设备连接")
    return deviceList
# 安装指定路径下的apk
@inforPrint
def installAPKFromPath(deviceId,path,*,beforeTime=1,endTime=1,infor=None):
    if mkCmdByPope("adb -s %s install -r %s",deviceId,path,sucess="Success")==True:
        if infor==None:
            infor=""
        print(deviceId+"："+infor+'成功')
        return True
    else:
        if infor==None:
            infor=""
        print(deviceId+"："+infor+'失败')
        return False
#回到桌面
@inforPrint
def returnHome(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope("adb -s %s shell input keyevent 3",deviceId)
#杀死指定进程
@inforPrint
def killAPP(deviceId,appPackage,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope("adb -s %s shell am force-stop %s",deviceId,appPackage)
#启动指定apk
@inforPrint
def startApp(deviceId,appPackageAndActivity,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope("adb -s %s shell am start -n %s",deviceId,appPackageAndActivity)
#点击指定坐标
@inforPrint
def tapXY(deiceId,X,Y,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope("adb -s %s shell input tap %s %s",deiceId,X,Y)
#在指定坐标输入文字
@inforPrint
def inputTextByXY(deviceId,X,Y,text,*,beforeTime=1,endTime=1,infor=None):
    tapXY(deviceId,X,Y)
    time.sleep(1)
    mkCmdByPope("adb -s %s shell input text %s",deviceId,text)
#输入文字
@inforPrint
def inputText(deviceId,text,phone,*,beforeTime=1,endTime=1,infor=None):
    if phone==config.PHONE_ZTE_BV0701:#如果是中兴小鲜
        tapXY(deviceId,224,1860)
        mkCmdByPope("adb -s %s shell input text %s", deviceId, text)
    elif phone==config.PHONE_COOLPAD:#如果是酷派
        if len(text)>=1:
            if text[0].isdigit():#以数字开头
                tapXY(deviceId, 160, 1211)
                mkCmdByPope("adb -s %s shell input text %s", deviceId, text)
            else:
                tapXY(deviceId, 103, 1251)
                mkCmdByPope("adb -s %s shell input text %s", deviceId, text)
        else:
            mkCmdByPope("adb -s %s shell input text %s", deviceId, text)
    elif phone==config.PHONE_M571C:#魅族
        for i in text:
            if i.isdigit():

                mkCmdByPope('adb -s %s shell input text %s',deviceId,i)
            else:
                if i.isupper():
                    tapXY(deviceId, 115, 1682)
                mkCmdByPope('adb -s %s shell input text %s', deviceId, i)
    else:mkCmdByPope('adb -s %s shell input text %s', deviceId, text)

#在指定目录新建文件夹
@inforPrint
def mkPath(deviceId,path,*,beforeTime=1,endTime=1,infor=None):
    if os.path.exists(path):
        pass
    else:
        #如果文件夹不存在
        os.mkdir(path)
    pass

#导出指定文件到指定目录
@inforPrint
def export(deviceId,fromPath,exportPath,*,beforeTime=1,endTime=1,infor=None):
    exportPath=exportPath+deviceId+"\\"
    mkPath(deviceId,exportPath)
    mkCmdByPope('adb -s %s pull %s %s',deviceId,fromPath,exportPath)
    pass
#导出当前UI界面到临时文件夹
def getNowUI(deviceId):
    mkCmdByPope('adb -s %s shell uiautomator dump /mnt/sdcard/%s.xml',deviceId,deviceId)
    if os.path.exists(config.TEMP_UI_XML_SAVE_PATH):
       if os.path.exists(config.TEMP_UI_XML_SAVE_PATH+deviceId+'.xml'):
           os.remove(config.TEMP_UI_XML_SAVE_PATH+deviceId+'.xml')
    else:
        os.mkdir(config.TEMP_UI_XML_SAVE_PATH)
    mkCmdByPope('adb -s %s pull /mnt/sdcard/%s.xml %s',deviceId,deviceId,config.TEMP_UI_XML_SAVE_PATH)
    mkCmdByPope('adb -s %s shell rm /mnt/sdcard/%s.xml',deviceId,deviceId)
#重启手机
@inforPrint
def reboot(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell reboot',deviceId)

#检查是否安装指定包的app
@inforPrint
def checkAPPIfInstall(deviceId,appPackage,*,beforeTime=1,endTime=1,infor=None):
    return mkCmdByPope("adb -s %s shell pm path %s",deviceId,appPackage,sucess='package:/data/app/')

#获取手机型号
@inforPrint
def getPhoneProduct(deviceId,*,beforeTime=1,endTime=1,infor=None):
    return mkCmdReturnInfor('adb -s %s shell getprop ro.product.model',deviceId)

#点击菜单键
@inforPrint
def tapMenu(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell input keyevent 1',deviceId)
#拖移动文件到设备指定目录
@inforPrint
def pushFile(deviceId,filePath,pushPath,*,beforeTime=1,endTime=1,infor=None):
    return mkCmdByPope('adb -s %s push %s %s',deviceId,filePath,pushPath,sucess='pushed')

#强制关闭app并清理数据
@inforPrint
def closeAPPAndClear(deviceId,packageName,*,beforeTime=1,endTime=1,infor=None):
    return mkCmdByPope("adb -s %s shell pm clear %s",deviceId,packageName,sucess='Success')
#点击
@inforPrint
def backKey(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell input keyevent 4',deviceId)
#从x1,y1滑动到x2,y2
@inforPrint
def swipe(deviceId,x1,y1,x2,y2,time=1000,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell input swipe %s %s %s %s %s',deviceId,x1,y1,x2,y2,time)

#新建文件夹
@inforPrint
def mkDir(deviceId,path,*,beforeTime=1,endTime=1,infor=None):
    #先判断是否存在这个文件夹
    if mkCmdByPope('adb -s %s shell cd %s',deviceId,path,sucess="No such file or directory")==False:
        #如果返回目录存在，则应先移除
        mkCmdByPope('adb -s %s shell rm %s',deviceId,path)
    #创建这个目录
    mkCmdByPope('adb -s %s shell mkdir -p %s',deviceId,path)

#输入中文第二步
@inforPrint
def inputTextForChinese(deviceId,text,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell am broadcast -a ADB_INPUT_TEXT --es msg \'%s\'',deviceId,text)
    pass
#截屏
@inforPrint
def getScreenpicture(deviceId,path,name,*,beforeTime=1,endTime=1,infor=None):
    fileName='/mnt/sdcard/%s.png' % name
    mkCmdByPope('adb -s %s shell /system/bin/screencap -p %s',deviceId,fileName)
    mkCmdByPope('adb -s %s pull %s %s ',deviceId,fileName,path)
#点击返回键
@inforPrint
def tapReturn(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell input keyevent 4',deviceId)

#退格
@inforPrint
def tapDel(deviceId,*,beforeTime=1,endTime=1,infor=None):
    mkCmdByPope('adb -s %s shell input keyevent 67', deviceId)