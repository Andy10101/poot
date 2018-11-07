import os
import adb
from io import StringIO
class ADB():

    def __init__(self,device_id:str):
        self._device_id=device_id
        self._cmd_prefix="adb -s %s " % device_id

    def returnHome(self):
        self.__make_cmd_by_pope("shell input keyevent 3")

    def getNowUI(self):
        '''
        如果没有成功取得ui文件，则返回False
        :return:
        '''
        self.__make_cmd_by_pope('shell uiautomator dump /mnt/sdcard/%s.xml', self._device_id)
        if os.path.exists(adb.TEMP_UI_XML_SAVE_PATH):
            if os.path.exists("%s/%s.xml" % (adb.TEMP_UI_XML_SAVE_PATH,self._device_id)):
                os.remove("%s/%s.xml" % (adb.TEMP_UI_XML_SAVE_PATH,self._device_id))
        else:
            os.mkdir(adb.TEMP_UI_XML_SAVE_PATH)
        if not self.__make_cmd_by_pope_return_sucess('pull /mnt/sdcard/%s.xml %s',self._device_id, adb.TEMP_UI_XML_SAVE_PATH,sucess="pulled"):
            self.__make_cmd_by_pope('shell rm /mnt/sdcard/%s.xml', self._device_id)
            return False
        self.__make_cmd_by_pope('shell rm /mnt/sdcard/%s.xml', self._device_id)
        return True
    def __make_cmd_by_pope(self,cmd,*args):
        '''
        无需返回结果，只要执行则认为成功
        :param cmd:shell
        :param args:
        :return:
        '''
        if (args!=None):
            cmd=self._cmd_prefix+(cmd % args)
        resault=os.popen(cmd)
        resault=resault.read()
        resault = resault.strip()
        if "no found" in resault:
            raise BaseException(adb.DEVICE_NOT_FOUND)
        return True
    def __make_cmd_by_pope_return_sucess(self,cmd,*args,sucess):
        '''
        此方法需要返回指定的sucess，否则认为执行失败
        :param cmd:
        :param args:
        :param sucess:
        :return:
        '''
        if (args!=None):
            cmd = self._cmd_prefix + (cmd % args)
        resault=os.popen(cmd)
        resault=resault.read()
        if sucess!=None:
            resault=resault.strip()
            if "no found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            if sucess in resault:
                return True
            else:
                return False
        return False
    def __make_cmd_by_pope_return_true_or_false(self,cmd,*args):
        '''
        只有有结果返回，即认为执行成功
        :param cmd:
        :param args:
        :return:
        '''
        if (args != None):
            cmd = self._cmd_prefix + (cmd % args)
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return True
        else:
            return False
    def __make_cmd_by_pope_return_re(self,cmd,*args):
        '''
        此方法返回执行后的结果
        :param cmd:
        :param args:
        :return:
        '''
        if (args != None):
            cmd = self._cmd_prefix + (cmd % args)
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return str(resault).strip()
