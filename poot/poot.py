#通过poot获取到将节点信息进行解析
from xml.dom.minidom import parse
import poot.by as By
from poot.uIProxy import Node,UiProxy
import xml.dom.minidom
class Poot():
    def __init__(self):
        self._first_node=None
    def __call__(self,tempxml,infor=None,by:By=By.text):
        if infor:
            #返回对应的节点代理ui
            proxy=self.__resolve_node(tempxml)
            return proxy.offspring(infor,by)
        else:
            #返回根节点代理ui
            return self.__resolve_node(tempxml)
    def __resolve_node(self,xml):
        DomTree=parse(xml)
        root_Node=DomTree.documentElement
        #传入xml文件信息，并解析其节点信息存储至node
        return UiProxy(root_Node)