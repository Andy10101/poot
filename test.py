from poot.poot import Poot,By
import os
poot=Poot()
xmlPath="%s/s.xml" % os.getcwd()

print(poot(xmlPath,"com.tencent.mm:id/dmc",By.resource_id).get_resource_id())