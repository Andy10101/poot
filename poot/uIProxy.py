import poot.by as By
from xml.dom.minidom import Text,Element


class Bound():
    #位置信息
    #[0,0][720,1280]
    def __init__(self,bounds:str):
        x1,y1=bounds.split("][")[0].split(",")
        x2,y2=bounds.split("][")[1].split(",")
        self._left_x=x1
        self._left_y=y1
        self._right_x=x2
        self._right_y=y2
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
        self._nodeinfor=nodeinfor
        self.__take_childs()
        self.__take_parent_node()

    def __resolve_attr(self):
        self.__take_bounds()
        attr_key=[""]
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
                    self._childs.append(child)

    def __take_parent_node(self):
        '''
        获得此节点的父节点
        :return:
        '''
        self._parent_node=self._nodeinfor.parentNode
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
    @property
    def resource_id(self):
        '''
        获取此节点的资源id，不存在返回None
        :return:
        '''
        return self.__take_attr("resource-id")
    @property
    def text(self):
        '''
        获取此节点的文字信息，如果不存在则返回None
        :return:
        '''
        return self.__take_attr("text")
    @property
    def clazz(self):
        return self._class
    @property
    def package(self):
        return self._package
    @property
    def content_desc(self):
        return self._content_desc
    @property
    def checked(self):
        return self._checked
    @property
    def clickable(self):
        return self._clickable
    @property
    def enabled(self):
        return self._enabled
    @property
    def focused(self):
        return self._focused
    @property
    def scrollable(self):
        return self._scrollable
    @property
    def long_clickable(self):
        return self._long_clickable
    @property
    def password(self):
        return self._password
    @property
    def selected(self):
        return self._selected
    @property
    def bounds(self):
        return self._bounds
    @property
    def father_node(self):
        return self._parent_node
    @property
    def childs(self):
        return self._childs
    @property
    def nodeinfor(self):
        return self._nodeinfor

class UiProxy():
    '''
    此类为ui控件的代理，通过解析xml文件生成。
    '''
    def __init__(self,nodes=None):#当前ui代理所代理的节点
        self._re_nodes=nodes  #原始dom节点
        self._nodes=[]
        if type(nodes)==type([]):#传入的是dom节点数组
            for node in nodes:
                self._nodes.append(Node(nodeinfor=node))
        else:#传入了单个dom节点
            self._nodes.append(Node(nodeinfor=nodes))#自建node节点
    def __getitem__(self, item):
        node_count=self.get_node_count()
        if item>=node_count:
            raise IndexError("索引超出")
        return UiProxy(self._nodes[item].nodeinfor)
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
            return UiProxy(all_node)
    def __traverse_node(self,node,infor=None,by:By=By.text):
        all_node=[]
        if infor:
            if by==By.part_text:
                if node.hasAttribute("text"):
                    if infor in node.getAttribute("text"):
                        all_node.append(node)
            else:
                if node.hasAttribute(by):
                    if infor==node.getAttribute(by):
                        all_node.append(node)
        else:
            all_node.append(node)
        if node.hasChildNodes():
            #如果这个节点存在子节点,则获取这些子节点
            childs=[]
            child_nodes = node.childNodes
            for child in child_nodes:
                if type(child) == Element:  # 只解析元素型节点，忽略文本型节点
                    childs.append(child)
            for child in childs:
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
                    if node.hasAttribute("text"):
                        if infor in node.getAttribute("text"):
                            all_node.append(node)
            else:
                for node in temp_all_node:
                    if node.hasAttribute(by):
                        if infor == node.getAttribute(by):
                            all_node.append(node)
        else:
            #返回所有子节点
            for node in self._nodes:
                #获取当前节点的子节点
                node=node.childs
                all_node+=node
            all_node=self.__del_same_node(all_node)
        if all_node:
            return UiProxy(nodes=all_node)
    def __del_same_node(self,all_node:[]):
        '''
        比较comper_node是否和all_node中的某一个node相同，如果相同则返回原始all_node,不相同则加入comper_node并返回
        :param all_node:
        :param comper_node:
        :return:
        '''
        for i in range(0,len(all_node)):
            for j in range(i+1,len(all_node)):
                if all_node[i].isSameNode(all_node[j]):
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


