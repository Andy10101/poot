import poot.by as By
from xml.dom.minidom import Element
from poot import inforPrint
from adb.adb import ADB
class Bound():
    #位置信息
    #[0,0][720,1280]
    def __init__(self,bounds:str):
        x1,y1=bounds.split("][")[0].split(",")
        x2,y2=bounds.split("][")[1].split(",")
        self._left_x=int(x1[1:])
        self._left_y=int(y1)
        self._right_x=int(x2)
        self._right_y=int(y2[0:-1])
    def __str__(self):
        return "[%s,%s][%s,%s]" % (self._left_x,self._left_y,self._right_x,self._right_y)
    @property
    def left_x(self):
        return self._left_x
    @property
    def left_y(self):
        return self._left_y
    @property
    def right_x(self):
        return self._right_x
    @property
    def right_y(self):
        return self._right_y

class Node():
    #节点信息类
    #包含了单个节点的所有信息
    def __init__(self,nodeinfor):
        self._childs=None
        self._bounds=None
        self._text=None
        self._resource_id=None
        self._parent_node=None
        self._clazz=None
        self._package=None
        self._index=None
        self._nodeinfor=nodeinfor
        self._value=Node
    def __str__(self):
        #[resource-id,text,desc,bounds]
        return " (%s)%s:%s %s" % (self.index,self.clazz,self.text,self.bounds)
    def __take_childs(self):
        '''
        获得子节点集合
        :return:
        '''
        self._childs = []
        if self._nodeinfor.hasChildNodes():
            #如果存在子节点
            child_nodes=self._nodeinfor.childNodes
            for child in child_nodes:
                if type(child)==Element:#只解析元素型节点，忽略文本型节点
                    self._childs.append(Node(child))
    def __take_parent_node(self):
        '''
        获得此节点的父节点
        :return:
        '''
        self._parent_node=Node(self._nodeinfor.parentNode)
    def __take_attr(self,attr_name):
        '''
        返回此节点对应的属性值，不存在返回None
        :param attr_name:
        :return:
        '''
        if self._nodeinfor.hasAttribute(attr_name):
            return self._nodeinfor.getAttribute(attr_name)
    def __take_bounds(self):
        '''
        解析此节点的位置信息
        :return:
        '''
        bounds=self.__take_attr("bounds")
        if bounds:
            self._bounds=Bound(bounds)
        else:
            self._bounds=None
    def is_same_node(self,node):
        '''
        判断当前节点和node节点是否来自同一个引用
        :param node:
        :return:
        '''
        return self._nodeinfor.isSameNode(node.nodeinfor)
    def have_any_childs(self):
        if self.childs:
            return True
        return False
    def get_attr(self,key):
        '''
        返回key对应的属性值，不存在则返回None
        :param key:
        :return:
        '''
        if key==By.bounds:
            return self.bounds
        return self.__take_attr(key)
    @property
    def bounds(self):
        if not self._bounds:
            self.__take_bounds()
        return self._bounds
    @property
    def father_node(self):
        if not self._parent_node:
            self.__take_parent_node()
        return self._parent_node
    @property
    def childs(self):
        if not self._childs:
            self.__take_childs()
        return self._childs
    @property
    def nodeinfor(self):
        return self._nodeinfor
    @property
    def text(self):
        if not self._text:
            self._text=self.__take_attr(By.text)
        return self._text
    @property
    def resource_id(self):
        if not self._resource_id:
            self._resource_id=self.__take_attr(By.resource_id)
        return self._resource_id
    @property
    def package(self):
        if not self._package:
            self._package=self.__take_attr(By.package)
        return self._package
    @property
    def clazz(self):
        if not self._clazz:
            self._clazz=self.__take_attr(By.clazz)
        return self._clazz
    @property
    def index(self):
        if not self._index:
            self._index=self.__take_attr(By.index)
        return self._index
    @property
    def value(self):
        if not self._value:
            self._value=self.__take_attr(By.value)
        return self._value
    @property
    def name(self):
        if not self._name:
            self._name=self.__take_attr(By.name)
        return self._name
class UiProxy():
    '''
    此类为ui控件的代理，通过解析xml文件生成。
    '''
    def __init__(self,nodes:[] or Node,adb:ADB):#当前ui代理所代理的节点
        self._nodes=[]
        self._adb=adb
        self._focus=(0.5,0.5)#ui的焦点，用于点击或者滑动
        if type(nodes)==type([]):#传入的是dom节点数组
            for node in nodes:
                self._nodes.append(node)
        else:#传入了单个dom节点
            self._nodes.append(nodes)#自建node节点
    def __getitem__(self, item):
        node_count=self.get_node_count()
        if item>=node_count:
            raise IndexError("索引超出")
        return UiProxy(self._nodes[item],self._adb)
    def offspring(self,infor=None,by:By=By.text):
        '''
        查找当前节点的后代节点（不仅限于子节点，也包括子节点的子节点）
        :param infor:
        :param by:
        :return:
        '''
        all_node = []
        if infor:#如果存在指定的查找条件
            for node in self._nodes:
                nodes = node.childs
                for node in nodes:
                    all_node += self.__traverse_node(node, infor=infor, by=by)#遍历此子节点下的所有节点，包括此子节点
                all_node=self.__del_same_node(all_node)#清除此节点列表里的重复节点引用
        else:
            for node in self._nodes:
                nodes = node.childs
                for node in nodes:
                    all_node += self.__traverse_node(node)#遍历此子节点下的所有节点，包括此子节点
                all_node=self.__del_same_node(all_node)#清除此节点列表里的重复节点引用
        if all_node:
            return UiProxy(all_node,self._adb)
    def __traverse_node(self,node:Node,infor=None,by:By=By.text):
        all_node=[]
        if infor:
            if by==By.part_text:
                if node.get_attr("text"):
                    if infor in node.get_attr("text"):
                        all_node.append(node)
            else:
                if node.get_attr(by):
                    if infor==node.get_attr(by):
                        all_node.append(node)
        else:
            all_node.append(node)
        if node.have_any_childs():
            #如果这个节点存在子节点,则获取这些子节点
            for child in node.childs:
                all_node+=self.__traverse_node(child,infor,by)
        return all_node
    def child(self,infor=None,by:By=By.text):
        '''
        查找子节点
        :param infor:
        :param by:
        :return: 如果存在子节点，则返回子节点，不存在则返回None
        '''
        all_node = []
        if infor:
            #指定查找对应子节点的text属性值来返回子节点的
            for node in self._nodes:
                #获取当前节点的子节点
                node=node.childs
                all_node+=node
            temp_all_node=self.__del_same_node(all_node)
            all_node=[]
            if by==By.part_text:
                for node in temp_all_node:
                    if node.get_attr("text"):
                        if infor in node.get_attr("text"):
                            all_node.append(node)
            else:
                for node in temp_all_node:
                    if node.get_attr(by):
                        if infor == node.get_attr(by):
                            all_node.append(node)
        else:
            #返回所有子节点
            for node in self._nodes:
                #获取当前节点的子节点
                node=node.childs
                all_node+=node
            all_node=self.__del_same_node(all_node)
        if all_node:
            return UiProxy(all_node,self._adb)
    def __del_same_node(self,all_node:[]):
        '''
        比较comper_node是否和all_node中的某一个node相同，如果相同则返回原始all_node,不相同则加入comper_node并返回
        :param all_node:
        :param comper_node:
        :return:
        '''
        for i in range(0,len(all_node)):
            for j in range(i+1,len(all_node)):
                if all_node[i].is_same_node(all_node[j]):
                    #比较2个节点
                    #如果此节点和后面某一个节点相同则将前一个节点至为None
                    all_node[i]=None
                    break
        return [node for node in all_node if node!=None]
    def is_single(self):
        '''
        判断是否是单个节点
        :return:
        '''
        if len(self._nodes)==1:
            return True
        else:
            return False
    def get_bounds(self):
        if len(self._nodes)>=1:
            return self._nodes[0].bounds
    def get_text(self):
        if len(self._nodes)>=1:
            return self._nodes[0].text
    def get_resource_id(self):
        if len(self._nodes)>=1:
            return self._nodes[0].resource_id
    def get_node_count(self):
        return len(self._nodes)
    def __get_tab(self,count):
        str=""
        for i in range(0,count):
            str+="-"
        return str
    def get_tree(self):
        if len(self._nodes)>=1:
            node=self._nodes[0]
            return self.__tree(node,0)
    def __tree(self,node,count):
        str="%s%s%s\n" % (count,self.__get_tab(count),node)
        if node.have_any_childs():
            childs=node.childs
            for child in childs:
                str+=self.__tree(child,count+1)
        return str
    def get_value(self):
        if len(self._nodes)>=1:
            return self._nodes[0].value
    @property
    def device_id(self):
        return self._adb.device_id

    def focus(self,focus:()):
        '''
        设置新的点击焦点
        :param focus:
        :return:
        '''
        if type(focus) != type((1,)):
            raise BaseException("焦点必须是元组")
        self._focus=focus
        return self


    @inforPrint(infor="返回桌面")
    def return_home(self,*,infor=None,beforeTime=0,endTime=0):
        self._adb.returnHome()
    @inforPrint(infor="点击")
    def tap(self,focus:()=None,*,infor=None,beforeTime=0,endTime=0):
        if len(self._nodes)>=1:
            node:Node=self._nodes[0]
            bound:Bound=node.bounds
            if focus:
                if type(focus)!=type((1,)):
                    raise BaseException("焦点必须是元组")
            else:
                focus=self._focus#使用预置焦点
            x_=(bound.right_x-bound.left_x)*focus[0]
            y_=(bound.right_y-bound.left_y)*focus[1]
            x=bound.left_x+x_
            y=bound.left_y+y_
            self._adb.tap_x_y(x,y)
        #self._adb.tap_x_y()