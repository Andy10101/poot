#设备模块：用来构造设备相关的方法
from device import baseDevice
from device import uiAnazed
#获取当前设备列表
getNowConnectDeviceList= baseDevice.getNowConnectDevice
#安装指定apk
installApkFromPath     = baseDevice.installAPKFromPath
#回到桌面
returnHome             = baseDevice.returnHome
#杀死指定app
killApp                = baseDevice.killAPP
#点击指定坐标
tapXY                  = baseDevice.tapXY
#在指定位置输入文字
inputTextByXY          = baseDevice.inputTextByXY
#启动指定app
startApp               = baseDevice.startApp
#检查是否安装指定app
checkAppIfInstall      = baseDevice.checkAPPIfInstall
#重启手机
reboot                 = baseDevice.reboot
#输入文字
inputText             = baseDevice.inputText
#返回手机型号
getPhoneProduct       = baseDevice.getPhoneProduct
#移动文件到设备指定位置
pushFile              = baseDevice.pushFile
#点击菜单键
tapMenu               = baseDevice.tapMenu
#清理app
closeAPPAndClear      = baseDevice.closeAPPAndClear
#滑动
swipe                 = baseDevice.swipe
#新建文件夹
mkDir                 = baseDevice.mkDir
#根据path建立文件夹
mkPath                =baseDevice.mkPath
#导指定文件到指定目录
export                =baseDevice.export
#点击返回
tapReturn             =baseDevice.tapReturn
#输入文字第二步
inputTextForChinese=baseDevice.inputTextForChinese
#获取截屏
getScreenpicture=baseDevice.getScreenpicture
#退格
tapDel=baseDevice.tapDel
backKey =baseDevice.backKey
getNowUi=baseDevice.getNowUI
#获取一个解析ui的实例
def getUiAnazaed(deviceId):
    return uiAnazed.UiAnazaed(deviceId)