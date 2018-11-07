from poot.poot import Poot
import poot.by as By
def test(deviceId):
    poot=Poot(deviceId)
    tree=poot("android.widget.ScrollView",By.clazz).offspring("我的信息",By.text).get_tree()