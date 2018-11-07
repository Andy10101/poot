from poot.poot import Poot,By
import os
#poot=Poot()
#xmlPath="%s/s.xml" % os.getcwd()
#print(poot(xmlPath).get_tree())
def f(c,*args,s):
    print(c)
    print(args)
    print(s)
Poot.getNowConnectDevice()

f(1,1,1,1,2,3,s=1)