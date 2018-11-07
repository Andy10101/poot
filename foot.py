from poot.poot import Poot
import poot.by as By
def test(deviceId):
    poot=Poot(deviceId)
    poot.get_wx_databases("c:\\temp")

