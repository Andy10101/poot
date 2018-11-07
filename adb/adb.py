import os
import adb
import re,hashlib
class ADB():
    def __init__(self,device_id:str):
        self._device_id=device_id
        self._cmd_prefix="adb -s %s " % device_id

    def tap_x_y(self,x,y):
        '''
        点击【x,y】对应的坐标点
        :param x:
        :param y:
        :return:
        '''
        self.__make_shell_by_pope("input tap %s %s",x,y)

    def returnHome(self):
        self.__make_cmd_by_pope("shell input keyevent 3")
    def rm_file(self,file):
        self.__make_shell_by_pope("rm %s" % file)
    def cp_src_file_to_dsc(self,src_file,dsc):
        '''
        将手机指定文件移动到指定位置
        :param src_file:
        :param dsc_file:
        :return:
        '''
        self.__make_shell_su_by_pope("cp %s %s",src_file,dsc)
    def pull_file_to_dsc(self,src_file,dsc):
        '''
        将src_file提取到电脑上的dsc文件夹
        :param src_file:
        :param dsc:
        :return:
        '''
        self.__make_cmd_by_pope_return_sucess('pull %s %s' % (src_file,dsc),sucess="pulled")
    def get_imei(self):
        res=self.__make_shell_by_pope_return_re("service call iphonesubinfo 1")
        imei1 = (re.compile(r"'[\.]+((\d\.)+)'").findall(res))[0][0]
        imei2 = (re.compile(r"'((\d\.)+)'").findall(res))[0][0]
        imei3 = (re.compile(r"'((\d\.)+).+ +'").findall(res))[0][0]
        imei1 = "".join(imei1.split("."))
        imei2 = "".join(imei2.split("."))
        imei3 = "".join(imei3.split("."))
        imei = imei1 + imei2 + imei3
        return imei
    def get_wx_databases(self,src):
        '''
        将微信数据库提取至【srv】目录,并计算其数据库密码
        :param src:
        :return:
        '''
        resautl=self.__make_shell_su_by_pope_return_re("ls /data/data/com.tencent.mm/MicroMsg")
        databases_path="/data/data/com.tencent.mm/MicroMsg/%s/EnMicroMsg.db" % resautl.split("\n\n")[0]
        self.cp_src_file_to_dsc(databases_path,"/mnt/sdcard/micro_db.db")
        self.pull_file_to_dsc("/mnt/sdcard/micro_db.db",src)
        self.rm_file("/mnt/sdcard/micro_db.db")
        self.cp_src_file_to_dsc("/data/data/com.tencent.mm/shared_prefs/system_config_prefs.xml","/mnt/sdcard/prefs.xml")
        self.rm_computer_file(adb.TEMP_XML)
        self.pull_file_to_dsc("/mnt/sdcard/prefs.xml",adb.TEMP_XML)
        self.rm_file("/mnt/sdcard/prefs.xml")
        with open(adb.TEMP_XML) as file:
            strs=file.read()
        uid=(re.compile(r'_uin" value="([-]*[\d]+)"').findall(strs))[0]
        self.rm_computer_file(adb.TEMP_XML)
        imei=self.get_imei()
        m2 = hashlib.md5()
        m2.update(("%s%s" % (imei,uid)).encode("utf-8"))
        return m2.hexdigest()[:7]
    def rm_computer_file(self,file):
        '''
        删除电脑上的文件
        :param file:
        :return:
        '''
        if os.path.exists(file):
            os.remove(file)
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
        if resault=="":
            return True
        else:
            return False
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
    def __make_shell_su_by_pope(self,cmd,*args):
        '''
        无需返回结果，只要执行返回“”则认为成功，否则认为失败
        :param cmd:shell
        :param args:
        :return:
        '''
        cmd_prefix=self._cmd_prefix+"shell su -c \""
        if (args!=None):
            cmd=cmd_prefix+(cmd % args)+"\""
        resault=os.popen(cmd)
        resault=resault.read()
        resault = resault.strip()
        if "no found" in resault:
            raise BaseException(adb.DEVICE_NOT_FOUND)
        if resault=="":
            return True
        else:
            return False
    def __make_shell_su_by_pope_return_sucess(self,cmd,*args,sucess):
        '''
        此方法需要返回指定的sucess，否则认为执行失败
        :param cmd:
        :param args:
        :param sucess:
        :return:
        '''
        cmd_prefix = self._cmd_prefix + "shell su -c \""
        if (args!=None):
            cmd = cmd_prefix + (cmd % args)+"\""
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
    def __make_shell_su_by_pope_return_true_or_false(self,cmd,*args):
        '''
        只有有结果返回，即认为执行成功
        :param cmd:
        :param args:
        :return:
        '''
        cmd_prefix = self._cmd_prefix + "shell su -c \""
        if (args != None):
            cmd = cmd_prefix + (cmd % args)+"\""
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return True
        else:
            return False
    def __make_shell_su_by_pope_return_re(self,cmd,*args):
        '''
        此方法返回执行后的结果
        :param cmd:
        :param args:
        :return:
        '''
        cmd_prefix=self._cmd_prefix + "shell su -c \""
        if (args != None):
            cmd = cmd_prefix + (cmd % args)+"\""
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return str(resault).strip()
    def __make_shell_by_pope(self,cmd,*args):
        '''
        无需返回结果，只要执行则认为成功
        :param cmd:shell
        :param args:
        :return:
        '''
        cmd_prefix = self._cmd_prefix + "shell "
        if (args!=None):
            cmd=cmd_prefix+(cmd % args)
        resault=os.popen(cmd)
        resault=resault.read()
        resault = resault.strip()
        if "no found" in resault:
            raise BaseException(adb.DEVICE_NOT_FOUND)
        if resault=="":
            return True
        else:
            return False
    def __make_shell_by_pope_return_sucess(self,cmd,*args,sucess):
        '''
        此方法需要返回指定的sucess，否则认为执行失败
        :param cmd:
        :param args:
        :param sucess:
        :return:
        '''
        cmd_prefix = self._cmd_prefix + "shell "
        if (args!=None):
            cmd = cmd_prefix + (cmd % args)
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
    def __make_shell_by_pope_return_true_or_false(self,cmd,*args):
        '''
        只有有结果返回，即认为执行成功
        :param cmd:
        :param args:
        :return:
        '''
        cmd_prefix = self._cmd_prefix + "shell "
        if (args != None):
            cmd = cmd_prefix+ (cmd % args)
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return True
        else:
            return False
    def __make_shell_by_pope_return_re(self,cmd,*args):
        '''
        此方法返回执行后的结果
        :param cmd:
        :param args:
        :return:
        '''
        cmd_prefix= self._cmd_prefix + "shell "
        if (args != None):
            cmd = cmd_prefix + (cmd % args)
        resault = os.popen(cmd)
        resault = resault.read()
        if resault:
            if "not found" in resault:
                raise BaseException(adb.DEVICE_NOT_FOUND)
            return str(resault).strip()
    @property
    def device_id(self):
        return self._device_id