import threader
import device
from foots import foot
#获取设备
try:
    deviceList=device.getNowConnectDeviceList()
    threader.startThrading(deviceList, foot.installWechatAndApp)
except BaseException as e:
    print("设备出错：",e)
