from poot.poot import Poot
import poot.by as By
def test(deviceId):
    poot=Poot(deviceId)
    poot("蓝牙").tap(infor="点击图库")

