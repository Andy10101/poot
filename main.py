import threader
from poot.poot import Poot
import foot
#获取设备
try:
    deviceList=Poot.getNowConnectDevice()
    threader.startThrading(deviceList, foot.test)
except BaseException as e:
    print("设备出错：",e)
