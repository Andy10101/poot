#通过poot获取到将节点信息进行解析
from xml.dom.minidom import parse
from poot import inforPrint
import poot.by as By
import time,os
from poot.uIProxy import Node,UiProxy
from adb.adb import ADB
import adb
import poot
from io import StringIO
class Poot():
    @staticmethod
    def getNowConnectDevice():
        str = os.popen('adb devices')
        str = str.read()
        f = StringIO(str)
        deviceList = []
        while True:
            s = f.readline()
            if s == '':
                break
            s = s.split()
            if s != [] and s[0] != 'List':
                deviceList.append(s[0])
        if deviceList == []:
            raise BaseException("当前未有设备连接")
        return deviceList
    def __init__(self,device_id:str):
        self._device_id=device_id #当前设备的连接id
        self._is_freeze=False  #是否处于冻结ui状态
        self._xml=None  #ui xml文件实列
        self._adb=ADB(self._device_id) #adb 实例
        self._time_out=30#获取ui的超时时间
        self._sleep_spacing=1#单次获取ui睡眠间隔
        self._sleep_count=self._time_out/self._sleep_spacing#获取ui睡眠次数
    def __call__(self,infor=None,by:By=By.text):
        if (not self._is_freeze) or (not self._xml):
            # 如果ui不是冻结的
            count=1
            while count<self._sleep_count:
                if not self._adb.getNowUI():
                    # 未获取到ui
                    count+=1
                    time.sleep(self._sleep_spacing)
                    continue
                self._xml = "%s/%s.xml" % (adb.TEMP_UI_XML_SAVE_PATH, self._device_id)
                if not os.path.exists(self._xml):
                    #未获取到ui
                    count+=1
                    time.sleep(self._sleep_spacing)
                    continue
                if infor:
                    # 返回对应的节点代理ui
                    proxy = self.__resolve_node(self._xml)
                    proxy=proxy.offspring(infor, by)
                    if not proxy:
                        count += 1
                        time.sleep(self._sleep_spacing)
                        continue
                    return proxy
                else:
                    # 返回根节点代理ui
                    return self.__resolve_node(self._xml)
            raise BaseException(poot.NOT_FOUND_UI)
        else:
            #如果是冻结的
            self._xml = "%s/%s.xml" % (adb.TEMP_UI_XML_SAVE_PATH, self._device_id)
            if not os.path.exists(self._xml):
                raise BaseException(poot.NOT_FOUND_UI)
            if infor:
                # 返回对应的节点代理ui
                proxy = self.__resolve_node(self._xml)
                proxy = proxy.offspring(infor, by)
                if not proxy:
                    raise BaseException(poot.NOT_FOUND_UI)
                return proxy
            else:
                # 返回根节点代理ui
                return self.__resolve_node(self._xml)
    def freeze(self):
        self._is_freeze=True
        return self
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_freeze=False
    def __resolve_node(self,xml):
        DomTree=parse(xml)
        root_Node=DomTree.documentElement
        node=Node(root_Node)
        #传入xml文件信息，并解析其节点信息存储至node
        return UiProxy(node,self._adb)
    def set_find_ui_timeout(self,timeout):
        '''
        设置获取ui的超时时间
        :param timeout:
        :return:
        '''
        self._time_out=timeout
    def set_find_ui_time_spacing(self,time_spacing):
        '''
        设置获取ui睡眠间隔时间
        :param time_spacing:
        :return:
        '''
        self._sleep_spacing=time_spacing
    @inforPrint
    def return_home(self,*,infor="回到桌面",beforeTime=1,endTime=1):
        '''
        回到桌面
        :return:
        '''
        self._adb.returnHome()
    @inforPrint
    def get_wx_databases(self,dsc,*,infor="获取微信数据库",beforeTime=1,endTime=1):
        return self._adb.get_wx_databases(dsc)