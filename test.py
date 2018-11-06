from poot.poot import Poot,By
import os
poot=Poot()
xmlPath="%s/s.xml" % os.getcwd()
print(poot(xmlPath).get_tree())
