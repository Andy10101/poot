#分析界面ui节点的函数
from device.baseDevice import *
import io
from xml.parsers.expat import ParserCreate
def inforPrint(fux):
    def wrapper(self,*args,**kwargs):
        if 'infor' in kwargs:
            if kwargs['infor']!=None:
                print(self._UiAnazaed__deviceId+'：'+kwargs['infor'])
        if 'beforeTime' in kwargs:
            if kwargs['beforeTime']!=0:
                time.sleep(kwargs['beforeTime'])
        temp=fux(self,*args,**kwargs)
        if 'endTime' in kwargs:
            if kwargs['endTime']!=0:
                time.sleep(kwargs['endTime'])
        return temp
    return wrapper

class UiAnazaed():
    def __init__(self,deviceId):
        self.__deviceId=deviceId
    #通过文字点击
    @inforPrint
    def tapByText(self,text,what=1,*,infor=None,beforeTime=1,endTime=0):
        self.__text=text
        self.__what = what
        self.__tempWhat = 1
        self.__ananazdUI(self.__anazedAttrTextAndTap)
    #等待特定文字出现
    @inforPrint
    def waitOpenByText(self,text,re=1,times=1,*,infor=None,beforeTime=1,endTime=0):
        self.__text=text
        self.__textBool=False
        i=1
        while True:
            if infor:
                print('第'+str(i)+'次'+infor)
            else:
                print('第' + str(i) + '次等待' )
            self.__ananazdUI(self.__ananazAttrTextAndFalseORTrue)
            if self.__textBool:
                return self.__textBool
            i=i+1
            if i>re:
                break
            else:
                time.sleep(times)
        return self.__textBool
        pass
    #通过特定资源id点击
    @inforPrint
    def tapById(self,id,what=1,*,infor=None,beforeTime=1,endTime=0):
        self.__id=id
        self.__what=what
        self.__tempWhat=1
        self.__ananazdUI(self.__ananzAttrResouceIDAndTap)
        pass
    #等待特定资源ID出现
    @inforPrint
    def waitOpenById(self,id,re=1,times=1,*,infor=None,beforeTime=1,endTime=0):
        self.__id = id
        self.__idBool = False
        i = 1
        while True:
            print('第' + str(i) + '次' + infor)
            self.__ananazdUI(self.__ananzAttrResouceAndFalseOrTrue)
            if self.__idBool:
                return self.__idBool
            i = i + 1
            if i > re:
                break
            else:
                time.sleep(times)
        return self.__textBool
        pass
    #等待特定资源id和特定文字出现
    @inforPrint
    def waitOpenByIDAndText(self,id,text,re=1,times=1,*,infor=None,beforeTime=1,endTime=0):
        self.__id = id
        self.__idBool = False
        self.__text = text
        self.__textBool = False
        i = 1
        while True:
            print('第' + str(i) + '次' + infor)
            self.__ananazdUI(self.__ananAttrRidAndTextAndFalseOrTrue)
            if self.__idBool and self.__textBool:
                return self.__idBool
            i = i + 1
            if i > re:
                break
            else:
                time.sleep(times)
        return False
        pass
    #检查特定资源是否开启
    @inforPrint
    def ifCheckedById(self,id,what=1,*,infor=None,beforeTime=1,endTime=0):
        self.__id=id
        self.__checked=False
        self.__what=what
        self.__tempWhat = 1
        self.__ananazdUI(self.__anazAttrIdIfChecked)
        return self.__checked
        pass
    #通过class点击
    @inforPrint
    def tapByClass(self,className,what=1,*,infor=None,beforeTime=1,endTime=0):
        self.__className=className
        self.__what=what
        self.__tempWhat=1
        self.__ananazdUI(self.__anazAttrClassAndTap)
    #等待某个package出现
    @inforPrint
    def waitOpenByPackage(self,packageName,re=1,times=2,*,infor=None,beforeTime=1,endTime=0):
        self.__packageName =packageName
        self.__packageNameBool = False
        i = 1
        while True:
            print('第' + str(i) + '次' + infor)
            self.__ananazdUI(self.__anazAttrPackageNameAndFalseOrTrue)
            if self.__packageNameBool:
                return self.__packageNameBool
            i = i + 1
            if i > re:
                break
            else:
                time.sleep(times)
        return self.__packageNameBool
        pass
    #从某个资源id滑动至另一个资源id
    @inforPrint
    def swipeFromIdToId(self,fromId,toId,time=1000,*,infor=None,beforeTime=1,endTime=0):
        self.__x1=None
        self.__y1=None
        self.__x2=None
        self.__y2=None
        self.__fromId=fromId
        self.__toId=toId
        self.__ananazdUI(self.__anazAttrIdReturnXY)
        swipe(self.__deviceId,self.__x1,self.__y1,self.__x2,self.__y2,time=time)
        pass
    #根据部分text返回全部text
    @inforPrint
    def getText(self,text,what=1,*,infor=None,beforeTime=1,endTime=0):
        self.__text = text
        self.__what = what
        self.__tempWhat = 1
        self.__ananazdUI(self.__anazedAttrTextAndReturn)
        if self._return_text:
            return self._return_text



    #解析UI
    def __ananazdUI(self,fux):
        # 得到当前ui
        getNowUI(self.__deviceId)
        # 从系统盘读取当前ui到内存
        file = None
        try:
            file = io.open(config.TEMP_UI_XML_SAVE_PATH + self.__deviceId+".xml", encoding='utf-8')
            # 将ui文件以字符串形式读取到内存
            ui = file.read()
            parser = ParserCreate()
            parser.StartElementHandler = fux
            parser.Parse(ui)
        except IOError as e:
            print('UI文件读取错误')
            return False
        finally:
            if file != None:
                file.close()
        pass
    #解析属性资源id,如果此id可以匹配，则记录
    def __anazAttrIdReturnXY(self,name,attr):
        if 'resource-id' in attr:
            if attr['resource-id'] == self.__fromId:
                if 'bounds' in attr:
                    temp=self.__anazedReturnPosition(attr['bounds'])
                    self.__x1=temp[0]
                    self.__y1=temp[1]
            if attr['resource-id'] == self.__toId:
                if 'bounds' in attr:
                    temp=self.__anazedReturnPosition(attr['bounds'])
                    self.__x2=temp[0]
                    self.__y2=temp[1]
    #解析属性资源id，如果此id可以匹配，则检查此id是否checked，如果checked，则self.__checked=True
    def __anazAttrIdIfChecked(self,name,attr):
        if 'resource-id' in attr:
            if attr['resource-id']==self.__id:
                if self.__tempWhat==self.__what:
                    if 'checked' in attr:
                        if attr['checked']=='true':
                            self.__checked=True
                            self.__what=-1
                else:
                    self.__tempWhat=self.__tempWhat+1
        pass
    #解析属性package，如果存在，则赋值
    def __anazAttrPackageNameAndFalseOrTrue(self,name,attr):
        if 'package' in attr:
            if attr['package']==self.__packageName:
                self.__packageNameBool=True
    #解析属性资id和text，如果这个资源id和text存在，则赋值
    def __ananAttrRidAndTextAndFalseOrTrue(self,name,attr):
        if 'resource-id' in attr:
            if attr['resource-id']==self.__id:
                self.__idBool=True
        if 'text' in attr:
            if attr['text']==self.__text:
                self.__textBool=True
        pass
    #解析属性资源id，如果这个资源id存在，则赋值self.__idBool为True
    def __ananzAttrResouceAndFalseOrTrue(self,name,attr):
        if 'resource-id' in attr:
            if attr['resource-id']==self.__id:
                self.__idBool=True
        pass
    #解析属性class，如果存在，则进行点击
    def __anazAttrClassAndTap(self,name,attr):
        if 'class' in attr:
            if attr['class']==self.__className:
                if self.__tempWhat==self.__what:
                    if 'bounds' in attr:
                        self.__anazedTapPositionAndTap(attr['bounds'])
                        self.__what = -1
                else:
                    self.__tempWhat = self.__tempWhat + 1
    #解析属性资源id,如果这个资源存在，则进行点击
    def __ananzAttrResouceIDAndTap(self,name,attr):
        if 'resource-id' in attr:
            if attr['resource-id']==self.__id:
                if self.__tempWhat==self.__what:
                    if 'bounds' in attr:
                        self.__anazedTapPositionAndTap(attr['bounds'])
                        self.__what=-1
                else:
                    self.__tempWhat=self.__tempWhat+1
    #解析text，如果text存在，赋值给self.__textBool为true
    def __ananazAttrTextAndFalseORTrue(self,name,attr):
        if 'text' in attr:
            if self.__text in attr['text']:
                self.__textBool=True
        pass
    #解析当前text的bounds属性并进行点击
    def __anazedAttrTextAndTap(self,name,attr):
        if 'text' in attr:
            if attr['text'] == self.__text:
                if self.__tempWhat==self.__what:
                    if 'bounds' in attr:
                        self.__anazedTapPositionAndTap(attr['bounds'])
                        self.__what = -1
                else:
                    self.__tempWhat=self.__tempWhat+1
    #根据bounds解析一个点击位置并点击
    def __anazedTapPositionAndTap(self,bounds):
        #对bounds进行解析
        temp = bounds.split('][')
        xy1 = temp[0][1:]
        xy2 = temp[1][:len(temp[1]) - 1]
        x1 = int(xy1.split(',')[0])
        y1 = int(xy1.split(',')[1])
        x2 = int(xy2.split(',')[0])
        y2 = int(xy2.split(',')[1])
        x=(x1+x2)/2
        y=(y1+y2)/2
        tapXY(self.__deviceId,x,y)
    #根据bounds解析一个位置并返回这个位置
    def __anazedReturnPosition(self,bounds):
        temp = bounds.split('][')
        xy1 = temp[0][1:]
        xy2 = temp[1][:len(temp[1]) - 1]
        x1 = int(xy1.split(',')[0])
        y1 = int(xy1.split(',')[1])
        x2 = int(xy2.split(',')[0])
        y2 = int(xy2.split(',')[1])
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (x,y)

    #解析当前text的text属性，并赋值给self._retrun_text
    def __anazedAttrTextAndReturn(self,name,attr):
        if 'text' in attr:
            if self.__text in attr['text'] :
                if self.__tempWhat==self.__what:
                    self._return_text=attr['text']
                    self.__what=-1
                else:
                    self.__tempWhat=self.__tempWhat+1