# 存储各个脚本函数
import device,time,traceback
import config,requests,json
from datetime import datetime
import math
def log(funx):
    def wrapper(*args, **kwargs):
        print("设备：" + args[0] + "开始执行脚本")
        if 'infor' in kwargs:
            if kwargs['infor'] != None:
                print('开始执行【' + kwargs['infor'] + '】脚本')
        funx(*args, **kwargs)
        print("设备：" + args[0] + "脚本执行结束")

    return wrapper
# 可重复使用脚本-------------------------------------------------------------------------------------------------
# 开启root授权和关闭默认安装监控：支持机型：酷派、小米4c、魅族
def startRoot(deviceId, phoneProuct):

    ui = device.getUiAnazaed(deviceId)
    device.returnHome(deviceId, infor='回到桌面')
    device.mkDir(deviceId, config.pushFileLocition)
    if phoneProuct==config.PHONE_XIAOMI_4A:
        print('无需设置')
        return
    flag=False
    if device.checkAppIfInstall(deviceId, 'com.kingroot.kinguser', infor='检查kingroot是否存在') == False:
        flag=True
        print('kinroot未安装,进行安装操作')
        if device.installApkFromPath(deviceId, config.new_kingroot, infor='安装Kingroot'):
            print('kingroot安装完成')
        else:
            print('kingroot安装失败,尝试再次安装')
    device.killApp(deviceId, 'com.kingroot.kinguser', infor='强制关闭kingroot')
    device.pushFile(deviceId, config.new_kingroot, config.pushFileLocition,infor='推送kINGroot到手机')
    if device.checkAppIfInstall(deviceId, 'com.kingroot.kinguser', infor='检查kingroot是否存在') == False:
        flag = True
        print('kinroot未安装,进行第二次安装操作')
        if device.installApkFromPath(deviceId, config.new_kingroot, infor='安装Kingroot'):
            print('kingroot安装完成')
        else:
            print(deviceId+'：第二次kingroot安装失败,如有需要，请手动安装或【重启手机】后再次尝试执行此脚本')
            return
    device.startApp(deviceId, 'com.kingroot.kinguser/.activitys.SliderMainActivity', infor='打开kingroot',beforeTime=2,endTime=1)
    if flag:
        if phoneProuct==config.PHONE_ZTE_BV0701:#如果是中兴小鲜
            device.swipe(deviceId, 535, 1500, 535, 150, infor='向上滑动',beforeTime=1)
            device.swipe(deviceId, 535, 1500, 535, 150, infor='向上滑动',beforeTime=1)
            device.tapXY(deviceId,561,1707,infor='点击立即开启',beforeTime=1)
        if phoneProuct==config.PHONE_M571C:#如果是魅族
            device.swipe(deviceId,577,1780,577,355,150,infor='向上滑动',beforeTime=1)
            device.swipe(deviceId, 577, 1780, 577, 355, 150, infor='向上滑动', beforeTime=1)
            device.swipe(deviceId, 577, 1780, 577, 355, 150, infor='向上滑动', beforeTime=1)
            device.tapXY(deviceId,607,1686,infor='点击立即开启',beforeTime=1)
        if ui.waitOpenByText('化繁为简',2,1,infor='是否出现化繁为简字样？'):
            ui.swipeFromIdToId('com.kingroot.kinguser:id/guide_arrow','com.kingroot.kinguser:id/guide_title',time=200,infor='向上滑动')
            ui.swipeFromIdToId('com.kingroot.kinguser:id/guide_arrow', 'com.kingroot.kinguser:id/guide_title', time=200,
                           infor='向上滑动')
            if ui.waitOpenByText('立即开启',2,1,infor='立即开启是否可见')==False:
                return
            ui.tapByText('立即开启',infor='点击立即开启')
    if ui.waitOpenByText('化繁为简', 2, 1, infor='是否出现化繁为简字样？'):
        ui.swipeFromIdToId('com.kingroot.kinguser:id/guide_arrow', 'com.kingroot.kinguser:id/guide_title', time=200,
                           infor='向上滑动')
        ui.swipeFromIdToId('com.kingroot.kinguser:id/guide_arrow', 'com.kingroot.kinguser:id/guide_title', time=200,
                           infor='向上滑动')
        if ui.waitOpenByText('立即开启', 2, 1, infor='立即开启是否可见') == False:
            return
        ui.tapByText('立即开启', infor='点击立即开启')
    if ui.waitOpenByText('KingRoot',2,1, infor='等待【KingRoot】字样可见') == False:
        return
    if ui.waitOpenByText('立即修复',2,1,infor='是否出现立即修复'):
        ui.tapByText('立即修复',infor='点击立即修复')
    if ui.waitOpenByText('立即处理',100,2,infor='立即处理是否出现')==False:
        print('kingroot主界面打开失败')
    #检查是否有root授权
    if ui.waitOpenById('com.kingroot.kinguser:id/left_button_device',2,1,infor='是否出现菜单按钮'):
        ui.tapById('com.kingroot.kinguser:id/left_button_device',infor='点击菜单按钮')
        if ui.waitOpenByText('已成功获取Root权限',2,1,infor='是否出现已成功获取Root权限字样')==False:
            if ui.waitOpenByText('重试',3,1,infor='是否出现重试？'):
                raise BaseException('获取ROOT失败，请手动获取后再继续执行。')
            if ui.waitOpenByText('立即修复', 5, 1, infor='是否出现立即修复'):
                ui.tapByText('立即修复', infor='点击立即修复')
                if ui.waitOpenByText('立即处理', 100, 2, infor='立即处理是否出现') == False:
                    print('权限修复失败，手动处理')
                    return
        ui.tapById('com.kingroot.kinguser:id/left_iv',infor='点击返回')
    #检查root授权结束

    ui.tapById('com.kingroot.kinguser:id/right_iv', 1, infor='点击右上角菜单')
    if phoneProuct == config.PHONE_COOLPAD:
        device.tapXY(deviceId, 558, 228, infor='酷派，使用坐标点击【通用设置】')
    else:
        ui.tapByText('通用设置', infor='点击【通用设置】')
    if ui.ifCheckedById('com.kingroot.kinguser:id/checkbox', infor='检查root授权是否开启'):
        print('root授权已开启')
    else:
        ui.tapById('com.kingroot.kinguser:id/checkbox', 1, infor='打开root授权')
    if ui.ifCheckedById('com.kingroot.kinguser:id/checkbox', 2, infor='检查【智能授权】是否开启'):
        print('智能授权已开启')
    else:
        ui.tapById('com.kingroot.kinguser:id/checkbox', 2, infor='开启【智能授权】')
    ui.tapByText('授权弹窗', infor='点击【授权弹窗】')
    ui.tapById('com.kingroot.kinguser:id/radio_button', infor='设置授权时间10s', beforeTime=2)
    ui.tapById('com.kingroot.kinguser:id/radio_button', 5, infor='设置授权【允许】', beforeTime=2)
    ui.tapById('com.kingroot.kinguser:id/left_iv', infor='点击【返回】按钮')
    if ui.waitOpenByText('高级权限管理', 1, 1, infor='等待高级权限管理字样可见') == False:
        ui.tapById('com.kingroot.kinguser:id/left_iv', infor='点击【返回】按钮')
    if ui.waitOpenByText('高级权限管理', 2, 1, infor='等待高级权限管理字样可见') == False:
        return
    ui.tapByText('高级权限管理', infor='点击高级权限管理')
    ui.tapByText('静默安装监控', infor='点击静默安装监控')
    if ui.waitOpenByText('立即开启', infor='检查是否有立即开启字样'):
        return
    ui.tapById('com.kingroot.kinguser:id/right_iv', infor='点击右上角菜单')
    ui.tapByText('停用监控', infor='点击停用监控')
    ui.tapByText('确定', infor='点击确定', beforeTime=2)
    ui.tapById('com.kingroot.kinguser:id/left_iv', infor='点击【返回】按钮')
    device.returnHome(deviceId, infor='回到桌面',beforeTime=1)
# 安装各个插件和移动文件支持机型：酷派、小米4c、魅族
def installAllPluags(deviceId, phoneProuct):
    ui = device.getUiAnazaed(deviceId)
    device.returnHome(deviceId, infor='回到桌面')
    if device.pushFile(deviceId, config.plugins, '/mnt/sdcard/', infor='推送plugins文件夹'):
        print(deviceId+'：推送成功')
    else:
        print(deviceId+'：推送失败')\
    #推送所有需要安装的软件
    device.pushFile(deviceId,config.new_chatproxy,config.pushFileLocition,infor='推送插件到手机')
    device.pushFile(deviceId, config.new_app, config.pushFileLocition, infor='推送APP到手机')
    #推送代码段结束
    device.installApkFromPath(deviceId, config.new_chatproxy, infor='安装chatproxy')


    device.installApkFromPath(deviceId, config.new_app, infor='安装有客到APP')



    print(deviceId + '：安装其他软件')
    for key, value in config.otherKeys:
        print(deviceId + '：正在安装' + key + ":" + value)
        device.pushFile(deviceId, value, config.pushFileLocition)
        device.installApkFromPath(deviceId, value)
    print(deviceId + '：其他软件安装结束')
    if phoneProuct == config.PHONE_M571C:  # 魅族
        device.pushFile(deviceId, config.new_Link2SD, config.pushFileLocition, infor='推送LINK2SD到手机')
        device.pushFile(deviceId, config.new_assisetScreen, config.pushFileLocition, infor='推送亮屏助手到手机')
        device.installApkFromPath(deviceId, config.new_Link2SD, infor='安装Link2SD')
        device.installApkFromPath(deviceId, config.new_assisetScreen, infor='安装屏幕助手')
    device.pushFile(deviceId,config.new_wechat, config.pushFileLocition, infor='推送微信到手机')
    device.installApkFromPath(deviceId,config.new_wechat,infor='更新微信')
    device.returnHome(deviceId, infor='回到桌面')
# 安装xp框架并启用xp框架 支持机型：酷派、小米4c、魅族
def xpCheck(deviceId, phoneProuct):
    ui = device.getUiAnazaed(deviceId)
    device.returnHome(deviceId, infor='回到桌面')
    if phoneProuct==config.PHONE_COOLPAD:#酷派
        device.pushFile(deviceId,config.new_xp_coolpad, config.pushFileLocition, infor='推送酷派框架到手机')
        device.installApkFromPath(deviceId,config.new_xp_coolpad,infor='安装酷派框架')
    else:
        device.pushFile(deviceId, config.new_xp, config.pushFileLocition, infor='推送框架到手机')
        device.installApkFromPath(deviceId,config.new_xp,infor='安装框架')
    pass
#setChat
def setChat(deviceId,phoneProuct):
    ui=device.getUiAnazaed(deviceId)
    device.returnHome(deviceId,infor='回到桌面')
    device.killApp(deviceId,'de.robv.android.xposed.installer',infor='关闭xp框架')
    device.startApp(deviceId,'de.robv.android.xposed.installer/de.robv.android.xposed.installer.WelcomeActivity',infor='打开xp框架')
    if ui.waitOpenByPackage('de.robv.android.xposed.installer',3,1,infor='等待xp打开')==False:
        raise BaseException('打开xp框架失败')
    if ui.waitOpenByText('小心！', 2, 1, infor='提示框是否存在？'):
        ui.tapById('de.robv.android.xposed.installer:id/md_promptCheckbox', infor='点击不再显示这个')
        ui.tapById('de.robv.android.xposed.installer:id/md_buttonDefaultPositive', infor='点击确定')
    if phoneProuct!=config.PHONE_COOLPAD:
        if ui.waitOpenByText('已激活', 2, 1, infor='是否安装xp框架')==False:
            raise BaseException('xp框架未刷入，请刷入xp框架再继续执行此脚本')
    if phoneProuct!=config.PHONE_COOLPAD:#酷派
       ui.tapByClass('android.widget.ImageButton',infor='打开菜单')
    ui.tapByText('模块',infor='点击模块')
    if ui.waitOpenById('de.robv.android.xposed.installer:id/checkbox',3,1,infor='等待模块界面打开')==False:
        raise BaseException('模块界面打开失败')
    if ui.ifCheckedById('de.robv.android.xposed.installer:id/checkbox',infor='是否勾选'):
        ui.tapById('de.robv.android.xposed.installer:id/checkbox',infor='去掉')
    ui.tapById('de.robv.android.xposed.installer:id/checkbox',infor='勾选',endTime=1)
    pass
#登录app
def login(deviceId,phoneProuct):
    device.returnHome(deviceId, infor='回到桌面')
    ui = device.getUiAnazaed(deviceId)
    device.killApp(deviceId,config.app_package_name,infor='关闭宜聚app')
    device.startApp(deviceId,config.app_package_name+'/com.youkedao.app.master.activity.IndexActivity',infor='打开APP',beforeTime=1)
    if phoneProuct==config.PHONE_M571C:#魅族
        if ui.waitOpenByPackage('android',2,1,infor='等待提示框打开？'):
            ui.tapByText('允许',infor='点击允许')
        if ui.waitOpenByPackage('com.kingroot.kinguser',2,1,infor='等待授权窗口打开?'):
            ui.tapById('com.kingroot.kinguser:id/button_right',infor='点击允许')
        if ui.waitOpenByText('登录',60,2,infor='等待app打开或者同步脚本')==False:
            raise BaseException('脚本同步失败，检查网络')
    elif phoneProuct==config.PHONE_COOLPAD:#酷派
        if ui.waitOpenByText('登录',60,2,infor='等待app打开或者同步脚本')==False:
            raise BaseException('脚本同步失败，检查网络')
        if ui.waitOpenByPackage('com.kingroot.kinguser', 2, 1, infor='等待授权窗口打开?'):
            ui.tapById('com.kingroot.kinguser:id/button_right', infor='点击允许')
    elif phoneProuct==config.PHONE_XIAOMI_4C:#小米4c
        if ui.waitOpenByText('安全警告',3,1,infor='是否弹出安全警告？'):
            ui.tapByText('允许',infor='点击允许')
        if ui.waitOpenByPackage('com.kingroot.kinguser', 3, 1, infor='等待授权窗口打开?'):
            ui.tapById('com.kingroot.kinguser:id/button_right', infor='点击允许')
        if ui.waitOpenByText('登录',60,2,infor='等待app打开或者同步脚本')==False:
            raise BaseException('脚本同步失败，检查网络')
    elif phoneProuct==config.PHONE_ZTE_BV0701:#中兴小鲜
        if ui.waitOpenByPackage('com.android.packageinstaller',3,1,infor='等待弹框出现'):
            ui.tapByText('始终允许',infor='点击【始终允许】')
        if ui.waitOpenByPackage(config.app_package_name,3,1,infor='等待APP打开')==False:
            raise BaseException('APP打开超时')
        if ui.waitOpenByText('登录',60,2,infor='等待【登录按钮出现】')==False:
            raise BaseException('同步脚本超时，请检查网络')
    elif phoneProuct==config.PHONE_RED_3 or phoneProuct==config.PHONE_RED_3S:#小米3
        if ui.waitOpenByText('安全警告', 3, 1, infor='是否弹出安全警告？'):
            ui.tapByText('允许', infor='点击允许')
        if ui.waitOpenByPackage('com.kingroot.kinguser', 3, 1, infor='等待授权窗口打开?'):
            ui.tapById('com.kingroot.kinguser:id/button_right', infor='点击允许')
        if ui.waitOpenByText('登录', 60, 2, infor='等待app打开或者同步脚本') == False:
            raise BaseException('脚本同步失败，检查网络')
    if ui.waitOpenByPackage('com.kingroot.kinguser',1,1,infor='是否提示静默安装拦截或者root授权'):
        ui.tapById('com.kingroot.kinguser:id/button_right',infor='点击允许')
    ui.tapById(config.app_package_name+':id/user_phone',infor='输入用户名',endTime=1)
    if ui.waitOpenByText('升级新版',2,1,infor='是否出现升级新版的提示？'):
        ui.tapByText('下次再说',infor='点击下次再说')
    device.inputText(deviceId,config.app_user,phoneProuct,endTime=1)
    ui.tapById(config.app_package_name+':id/user_pwd',infor='输入密码',endTime=1)
    device.inputText(deviceId,config.app_pwd,phoneProuct,endTime=1)
    ui.tapByText('登录',infor='点击登录')
    if ui.waitOpenByPackage('com.kingroot.kinguser',3,1,infor='是否提示静默安装拦截或者root授权'):
        ui.tapById('com.kingroot.kinguser:id/button_right',infor='点击允许')
    if ui.waitOpenByPackage('com.kingroot.kinguser',3,1,infor='是否提示静默安装拦截或者root授权'):
        ui.tapById('com.kingroot.kinguser:id/button_right',infor='点击允许')
    finMath(deviceId,phoneProuct)

#魅族登录后的特殊操作
def finMath(deviceId,phoneProuct):
    ui = device.getUiAnazaed(deviceId)
    if phoneProuct==config.PHONE_M571C:
        #获取宜聚二字
        device.returnHome(deviceId, beforeTime=10, infor='回到桌面')
        device.startApp(deviceId,'com.meizu.filemanager/com.meizu.flyme.filemanager.activity.FileManagerActivity')
        device.pushFile(deviceId,config.text_yiju,config.pushFileLocition)
        if ui.waitOpenByText('APushFile',3,1,infor='等待打开'):
            ui.tapByText('APushFile')
            ui.tapByText('atemp')
            ui.tapByText('HTML 查看程序')
            if ui.waitOpenByText('选择打开方式',3,1,infor='等待打开')==False:
                return
            device.swipe(deviceId,100,400,100,400,2000,beforeTime=1)
            ui.tapById('com.android.webview:id/select_action_menu_select_all')
            ui.tapById('com.android.webview:id/select_action_menu_copy')
            device.returnHome(deviceId,beforeTime=1,infor='回到桌面')
            device.startApp(deviceId,'com.buak.Link2SD/com.buak.Link2SD.Link2SD',beforeTime=1,infor='打开linksd')
            if ui.waitOpenByPackage('com.kingroot.kinguser',3,1,infor='是否出现弹窗'):
                ui.tapById('com.kingroot.kinguser:id/button_right')
            if ui.waitOpenByText('更新内容',3,1,infor='是否出现更新内容弹窗'):
                ui.tapByText('确定')
            if ui.waitOpenByText('Link2SD',10,1,infor='是否出现')==False:
                return
            ui.tapById('com.buak.Link2SD:id/menu_more',infor='点击【更多】')
            ui.tapByText('搜索',infor='点击【搜索】')
        #为了输入一个【宜聚】
            ui.tapByText('搜索程序',infor='点击搜索程序',beforeTime=1)
            device.tapXY(deviceId,189,349,beforeTime=1,infor='点击粘贴')
        #结束
            if ui.waitOpenById('com.buak.Link2SD:id/app_icon',3,1,infor='等待'):
                ui.tapById('com.buak.Link2SD:id/app_icon')
            else:
                return
            if ui.waitOpenById('com.buak.Link2SD:id/appdetails_menu_actions',3,1,infor='等待'):
                ui.tapById('com.buak.Link2SD:id/appdetails_menu_actions')
            else:
                return
            ui.tapByText('转换成系统应用',beforeTime=1)
            ui.tapByText('确定',beforeTime=1)
            device.reboot(deviceId,beforeTime=10)
# 自己编写脚本----------------------------------------------------------------------------------------------------

#登录前的操作
def installNewSofter(deviceId):
    ui = device.getUiAnazaed(deviceId)
    phoneProduct = device.getPhoneProduct(deviceId)
    startRoot(deviceId, phoneProduct)
    installAllPluags(deviceId, phoneProduct)
    xpCheck(deviceId, phoneProduct)
    device.startApp(deviceId, 'de.robv.android.xposed.installer/de.robv.android.xposed.installer.WelcomeActivity',
                    infor='打开xp框架')
    if ui.waitOpenByPackage('de.robv.android.xposed.installer', 3, 1, infor='等待xp管理器打开') == False:
        print('xp管理器打开失败')
    if ui.waitOpenByPackage('de.robv.android.xposed.installer', 3, 1, infor='等待xp管理器打开') == False:
        print('xp管理器打开失败')
        return
    if phoneProduct == config.PHONE_COOLPAD:  # 酷派特殊处理
        if ui.waitOpenByText('最新版本的 Xposed 当前未激活', 3, 1, infor='xp框架是否安装'):
            ui.tapById('android:id/text2', 1, infor='点击框架')
            if ui.waitOpenByText('小心！', 2, 1, infor='是否出现小心提示框？'):
                ui.tapByText('不要再显示这个', infor='点击不要再显示这个')
                ui.tapByText('确定', infor='点击确定')
            ui.tapById('de.robv.android.xposed.installer:id/btnInstall', infor='点击安装/更新')
            if ui.waitOpenByPackage('com.kingroot.kinguser', 3, 1, infor='等待授权窗口打开'):
                ui.tapByClass('android.widget.Button', 2, infor='点击允许')
            if ui.waitOpenByText('您现在要重启吗', 3, 1, infor='是否出现重启提示框'):
                ui.tapByText('确定', infor='点击确定')
        return

    if ui.waitOpenByText('小心！', 3, 1, infor='提示框是否存在？'):
        ui.tapById('de.robv.android.xposed.installer:id/md_promptCheckbox', infor='点击不再显示这个')
        ui.tapById('de.robv.android.xposed.installer:id/md_buttonDefaultPositive', infor='点击确定')
    if ui.waitOpenByText('已激活', 2, 1, infor='是否安装xp框架'):
        print("已安装XP框架")
        return
    if ui.waitOpenByText('Version 89', 5, 2, infor='89版是否可见？') == False:
        print('网络可能存在问题，请手动安装')
        return
    ui.tapByText('Version 89', infor='安装89框架')
    ui.tapByText('Install', infor='点击刷入')
#登录后的操作
def star(deviceId):
    ui = device.getUiAnazaed(deviceId)
    phoneProduct = device.getPhoneProduct(deviceId)
    setChat(deviceId, phoneProduct)
    login(deviceId, phoneProduct)
#操作


@log
def install(deviceId):
    try:
        if device.checkAppIfInstall(deviceId, "de.robv.android.xposed.installer", infor='是否安装XP框架'):
            print(deviceId+'：已安装，执行登录APP操作')
            star(deviceId)
        else:
            print(deviceId + '：未安装，执行安装APP操作')
            installNewSofter(deviceId)
    except BaseException as e:
        print('脚本执行错误，请截屏发送给脚本编辑人员', e)
        traceback.print_exc()
        time.sleep(10)
    finally:
        pass
@log
def test(deviceId):
    try:
        ui = device.getUiAnazaed(deviceId)
        phoneProduct = device.getPhoneProduct(deviceId)
        finMath(deviceId,phoneProduct)
    except BaseException as e:
        print(e)
    finally:
        print('结束')


#更新app
@log
def update(deviceId):
    try:
        ui = device.getUiAnazaed(deviceId)
        phone=device.getPhoneProduct(deviceId)
        device.returnHome(deviceId, infor='回到桌面')
        device.mkDir(deviceId, config.pushFileLocition)
        if device.pushFile(deviceId, config.plugins, '/mnt/sdcard/', infor='推送plugins文件夹'):
            print(deviceId + '：推送成功')
        else:
            print(deviceId + '：推送失败')
                # 推送所有需要安装的软件
        device.pushFile(deviceId, config.new_chatproxy, config.pushFileLocition, infor='推送插件到手机')
        device.pushFile(deviceId,config.new_app,config.pushFileLocition,infor='推送app')
        # 推送代码段结束
        device.installApkFromPath(deviceId, config.new_chatproxy, infor='安装chatproxy')
        device.installApkFromPath(deviceId,config.new_app,infor='安装app')
        device.returnHome(deviceId, infor='回到桌面')
        setChat(deviceId,phone)
        if ui.waitOpenById('de.robv.android.xposed.installer:id/checkbox', 3, 1, infor='等待模块界面打开'):
            device.reboot(deviceId,beforeTime=5,infor='5秒后自动重启')
        pass
    except BaseException as e:
        print(e)
    finally:
        print('结束')


#安装微信
@log
def udateWechat(deviceId):
    try:
        device.returnHome(deviceId, infor='回到桌面')
        device.installApkFromPath(deviceId, config.new_wechat, infor='更新微信')
        device.returnHome(deviceId, infor='回到桌面')
        pass
    except BaseException as e:
        print(e)
    finally:
        print('结束')
#导二维码到电脑
@log
def getQR(deviceId):
    device.mkPath(deviceId,'d:\\QR\\')
    phone=device.getPhoneProduct(deviceId)
    if phone==config.PHONE_XIAOMI_4A or phone==config.PHONE_RED_3 or phone==config.PHONE_RED_3S:
        device.export(deviceId, '/mnt/sdcard/DCIM/Screenshots/', 'd:\\QR\\')
    else:
        device.export(deviceId,'/mnt/sdcard/pictures/Screenshots/','d:\\QR\\')

#实际建群的方法,由某一个具体的设备调用建立具体的一个群
def _makeGroupMethod(deviceId,realGroupName,ms1,ms2,qrname):
    #获取建群信息
    phone=device.getPhoneProduct(deviceId)
    device.startApp(deviceId,'com.tencent.mm/com.tencent.mm.ui.LauncherUI',infor='打开微信',endTime=2)
    ui=device.getUiAnazaed(deviceId)
    if not ui.waitOpenById('com.tencent.mm:id/gd',20,1,infor='等待【+】出现'):
        raise BaseException(deviceId+'未出现微信主界面')
    ui.tapById('com.tencent.mm:id/gd',1,infor='点击【+】')
    ui.tapByText('发起群聊',infor='点击【发起群聊】')
    if not ui.waitOpenByIDAndText('android:id/text1','发起群聊',40,1,infor='等待【发起群聊界面出现】'):
        raise BaseException(deviceId+'未出现发起群聊界面')
    ui.tapById('com.tencent.mm:id/arx',1,infor='点击【搜索】框')
    device.inputTextForChinese(deviceId,ms1,infor='输入小号1')
    device.tapXY(deviceId,400,574,infor='点击小号1',beforeTime=2)
    device.inputTextForChinese(deviceId,ms2,infor='输入小号2')
    device.tapXY(deviceId, 400, 574, infor='点击小号2',beforeTime=2)
    ui.tapById('com.tencent.mm:id/hh',1,infor='点击【确定】')
    if not ui.waitOpenByText('群聊',35,2,infor='等待【群聊建立成功'):
        raise BaseException(deviceId+'群聊建立失败')
    ui.tapById('com.tencent.mm:id/hi',1,infor='点击【小人】')
    if not ui.waitOpenByText('聊天信息',30,1,infor='等待【聊天信息界面】开启'):
        raise BaseException(deviceId+'聊天信息界面开启失败')
    ui.tapByText('群聊名称',infor='点击【群聊名称】')
    if not ui.waitOpenByText('群名片',30,1,infor='等待【群名片】打开'):
        raise BaseException(deviceId + '群名片界面开启失败')
    ui.tapById('com.tencent.mm:id/cbt',1,infor='点击输入框')
    device.inputTextForChinese(deviceId,realGroupName,infor='输入群名')
    ui.tapByText('保存',infor='点击【保存】')
    if not ui.waitOpenByText('聊天信息',30,1,infor='等待【聊天信息界面】开启'):
        raise BaseException(deviceId+'聊天信息界面开启失败')
    ui.tapByText('群二维码',infor='点击【群二维码】')
    if not ui.waitOpenByText('该二维码7天内',50,2,infor='等待二维码出现'):
        raise BaseException(deviceId+'二维码生成失败')
    device.getScreenpicture(deviceId,'d:\\temp\\',qrname,infor='二维码截屏成功')
    device.tapReturn(deviceId, beforeTime=1)
    device.swipe(deviceId,588,1644,590,329,500,infor='向下滑动',beforeTime=1)
    ui.tapById('com.tencent.mm:id/gt',2,infor='点击置顶聊天')
    ui.tapById('com.tencent.mm:id/gt',3,infor='点击保存到通讯录')
    device.tapReturn(deviceId,beforeTime=1)
    device.tapReturn(deviceId,beforeTime=1)
    device.tapReturn(deviceId,beforeTime=1)
    device.returnHome(deviceId,infor='回到桌面',beforeTime=1)
    pass
#建一组群的方法
@log
def makeGroup(deviceId):
        idToGroupName = {'81CEBMQ225VC': ['玩游戏包脱单交流群', 'YC+A00', 'qgidtygd64247', 'andydytd09359'],
                         '81CEBMQ226K9':['游戏资深玩家交流会','YC+A01','wccgrp9i44235','qqygdnag05017'],
                         '81CEBMQ2263Q':['游戏头号玩家群','YC+A02','ytpqgsnd0391','ncaynati8433'],
                         '81CEBN42542S':['H5游戏嗨皮群','YC+A03','iadcrdto8127','tgdcyggg80895'],
                         '81CEBMM226RF':['魔性小游戏交流群','YC+A04','dtojghta6424','nhgncdc935194'],
                         '81CEBN6222WC':['游戏神经病玩家群','YC+A05','jilgntn936803','dwcoaagg84967'],
                         '81CEBMR226BX':['游戏深度患者交流群','YC+A06','kilauua934344','ddjcqdgy32524'],
                         '81CEBMM225FD':['游戏戒瘾交流群','YC+A07','imbatayc7330','hrtbnhyh7170'],
                         '81CEBMQ227GX':['游戏宅男进化群','YC+A08','igndhnit82608','fnuyigih30158'],
                         '81CEBME22BPY':['游戏男神交流会','YC+A09','qadyigdd7878','ahnvdyai62293'],
                         '81CEBN4252GB':['游戏奇葩交友会','YC+A10','nyydjtiy6297','yfyaiyng15738'],
                         'dededc2b7d53':['高能游戏交流群','YC+A12','shcorft945336','yqikati909936'],
                         '11846713':['游戏脱单男女群','YC+A11','idyccdc93605','itgtuidh47408'],
                         'ZTEC880A':['女神玩家男神玩家大家庭','YC+A14','egaewhdi39573','ntbydggd04504'],
                         'ZTEBV0720':['游戏独孤患者交友群','YC+A13','ntvacvdi72746','dxwdhhdn97315']
                         }
        if deviceId in idToGroupName:
            groupName = idToGroupName[deviceId][0]
            assertNumber = idToGroupName[deviceId][1]
            ms1 = idToGroupName[deviceId][2]
            ms2 = idToGroupName[deviceId][3]
        else:
            device.returnHome(deviceId, infor='回到桌面')
            raise BaseException(deviceId + '未找到对应群名，请检查，已回到桌面')
        groupPostfixs = ['08', '09', '10']
        for postfix in groupPostfixs:
            realGroupName = groupName + postfix
            qrname = assertNumber + postfix
            print(assertNumber + "：开始建立【" + realGroupName + "】")
            ui=device.getUiAnazaed(deviceId)
            _makeGroupMethod(deviceId, realGroupName, ms1, ms2, qrname)



#中兴小鲜：没问题
#红米3和3s：1、安装软件的时候会被拦截，需要手动点允许通过。其他没问题
#酷派：1、微信更新需要手动点击安装;2、第一次打开app会卡死，在执行程序前最好先进入一次，然后用最近任务栏强制关闭。其他没问题
#魅族：没问题，
#小米4c:没问题
#小米4a:1、安装软件的时候会被拦截，需手点击允许，其他没问题
#中兴a2:1、但是a1多台设备连接无法同时跑，其他没问题


#读取陌陌聊天界面
#获取单一图片链接
def getPictureLink(deviceId):
    ui=device.getUiAnazaed(deviceId)
    ui.tapById('com.immomo.momo:id/btn_feed_more',infor='点击分享')
    if not ui.waitOpenByText('QQ好友',1,1,infor='等待QQ好友出现'):
        return
   # ui.tapByText('QQ好友',infor='点击QQ好友')
    device.tapXY(deviceId,895,1310,infor='点击QQ好友')
    time.sleep(1.2)
    #ui.tapByText('我的电脑',infor='点击我的电脑')
    device.tapXY(deviceId,435,683,infor='点击我的电脑')
   # ui.tapByText('发送',infor='点击发送')
    time.sleep(0.5)
    device.tapXY(deviceId,779,1211,infor='点击发送')
    time.sleep(0.5)
    #ui.tapByText('返回MOMO陌陌',infor='点击返回陌陌')
    device.tapXY(deviceId, 390, 1107, infor='点击返回')
    pass
#向下滑动
def swipeDown(deviceId):
    device.swipe(deviceId,561,1652,551,1000,500,infor='向上滑动',beforeTime=1)
    pass
def getMomo(deviceId):
    recodeTime=datetime.now()
    while True:
        getPictureLink(deviceId)
        swipeDown(deviceId)
        time=datetime.now()-recodeTime
        if time.seconds>1500:
            break

def logout(deviceId):
    '''
    退出登陆
    :param deviceId:
    :return:
    '''
    device.returnHome(deviceId, infor='回到桌面')
    ui = device.getUiAnazaed(deviceId)
    device.killApp(deviceId, config.app_package_name, infor='关闭宜聚app')
    device.startApp(deviceId, config.app_package_name + '/com.youkedao.app.master.activity.IndexActivity',
                    infor='打开APP', beforeTime=1)
    ui.tapByText("我的",infor="点击我的")
    ui.tapByText("退出登陆",infor='点击退出登陆')
    ui.tapByText("确认退出",infor='点击确认退出')

@log
def band_phone(deviceId):
    ui=device.getUiAnazaed(deviceId)

    device.startApp(deviceId,"com.ykt.app.master/com.youkedao.app.master.activity.IndexActivity",infor='打开app')
    ui.waitOpenByText("有客团",50,1,infor="等待有客团打开")
    ui.tapByText("配置",infor='点击配置')
    if not ui.waitOpenByText("已暂停",2,1):
        ui.tapByText("暂停任务引擎",infor='点击暂停任务引擎')
        ui.tapByText("确认",infor="点击确认")
    device.killApp(deviceId,"com.tencent.mm",infor='关闭微信')
    device.startApp(deviceId, 'com.tencent.mm/com.tencent.mm.ui.LauncherUI', infor='打开微信', endTime=2)
    if not ui.waitOpenByText("微信",50,1,infor='等待微信打开'):
        raise BaseException("微信打开失败")
    ui.tapById("com.tencent.mm:id/b0w",4,infor='点击我')
    if not ui.waitOpenByText("设置",3,1,infor="等待设置打开"):
        ui.tapById("com.tencent.mm:id/cw2",4,infor="点击我")
    wechatid = ui.getText("微信号：", infor='获取微信号')
    wechatid=wechatid.split("：")[1]
    count = 1
    phone_n=None
    while True:
        rsponse = requests.get("http://www.junx.ink/get_phone.html")
        resault = json.loads(rsponse.text)
        if not resault["state"] == "success":
            count += 1
            time.sleep(5)
            if count >= 100:
                raise BaseException("得到手机号超时")
            print("%s：等待获取手机号中。。" % deviceId)
            continue
        phone_n = resault["phone"]
        # 输入验证码
        break
    if wechatid:
        #写日志
        rsponse = requests.get("http://www.junx.ink/add_log.html?foot_name=绑定手机号&log_infor=【%s】%s" % (wechatid,phone_n))
        json.loads(rsponse.text)
    else:
        #写日志
        rsponse = requests.get(
            "http://www.junx.ink/add_log.html?foot_name=绑定手机号&log_infor=【%s】%s" % ("未知", phone_n))
        json.loads(rsponse.text)
    ui.tapByText("设置",infor="点击设置",endTime=1)
    ui.tapByText("帐号与安全",infor="点击账号与安全",beforeTime=1)
    ui.tapByText("手机号",infor="点击手机号",beforeTime=1)
    ui.tapByText("绑定手机号",2,infor="点击绑定手机号",beforeTime=1)
    ui.tapByText("中国",infor="点击中国",beforeTime=1)
    ui.tapById("com.tencent.mm:id/bc",infor="点击搜索",beforeTime=1)
    ui.tapById("com.tencent.mm:id/bq", infor="点击搜索", beforeTime=1)
    phone=device.getPhoneProduct(deviceId)
    device.inputText(deviceId,"95",phone,infor="输入95",beforeTime=1)
    ui.tapByText("缅甸",infor='点击缅甸',beforeTime=1)
    ui.tapByText("你本人的手机号",infor='点击输入框',beforeTime=1)

    device.inputText(deviceId, phone_n, phone, infor='输入手机号', beforeTime=1)
    #device.inputText(deviceId,"09763388078",phone,infor='输入手机号',beforeTime=1)

    ui.tapByText("下一步",infor='点击下一步',beforeTime=1)
    ui.tapByText("确定",infor='点击确定',beforeTime=2)
    while True:
        ui.waitOpenByText("填写验证码",re=120,times=3,infor='等待输入框')
        ui.tapById("com.tencent.mm:id/xa",infor='点击输入框')
        count = 1
        while True:
            rsponse = requests.get("http://www.junx.ink/get_check_code.html?phone=%s" % phone_n)
            resault = json.loads(rsponse.text)
            if not resault["state"] == "success":
                count += 1
                time.sleep(5)
                if count >= 100:
                    raise BaseException("输入验证码超时")
                print("%s：等待【%s】获取验证码中。。" % (deviceId, phone_n))
                continue
            code = resault["code"]
            #输入验证码
            device.inputText(deviceId,str(code),phone,infor='输入验证码')
            break
        ui.tapByText("下一步",infor='点击下一步')
        if ui.waitOpenByText("确定",3,1,infor="验证码是否错误？"):
            ui.tapByText("确定",infor="点击确定")
            device.tapDel(deviceId)
            device.tapDel(deviceId)
            device.tapDel(deviceId)
            device.tapDel(deviceId)
            device.tapDel(deviceId)
            requests.get("http://www.junx.ink/set_check_able.html?phone=%s&able=2" % phone_n)
            json.loads(rsponse.text)
        else:
            requests.get("http://www.junx.ink/set_check_able.html?phone=%s&able=1" % phone_n)

            json.loads(rsponse.text)
            break
    if ui.waitOpenByText("完成",5,2,infor="等待完成"):
        device.returnHome(deviceId,beforeTime=2,infor="回到桌面")
        device.startApp(deviceId, "com.ykt.app.master/com.youkedao.app.master.activity.IndexActivity", infor='打开app')
        ui.waitOpenByText("有客团", 50, 1, infor="等待有客团打开")
        ui.tapByText("配置", infor='点击配置')
        if ui.waitOpenByText("已暂停", 2, 1):
            ui.tapByText("恢复任务引擎", infor='点击恢复任务引擎')
            ui.tapByText("确认", infor="点击确认")
import os
#更新配置文件和重启
@log
def downconfig(deviceId):
    device.pushFile(deviceId,os.getcwd()+r"\config.properties","/mnt/sdcard/com.clqf.app.master",infor='推送文件',beforeTime=2)
    device.reboot(deviceId,infor='重启')
    #退出


    pass

@log
def installWechatAndApp(deviceId):
    device.mkDir(deviceId,"/mnt/sdcard/0001",infor='建立存储文件夹')
    device.pushFile(deviceId,config.new_wechat,"/mnt/sdcard/0001",infor='推送微信')
    device.pushFile(deviceId,config.new_app,"/mnt/sdcard/0001",infor="推送App")
    device.pushFile(deviceId,config.new_xp,"/mnt/sdcard/0001",infor="推送寻")
    device.pushFile(deviceId,config.new_xp_coolpad,"/mnt/sdcard/0001",infor="推送xp")
    device.pushFile(deviceId,config.new_Link2SD,"/mnt/sdcard/0001",infor="推送2d")
    device.pushFile(deviceId,config.new_assisetScreen,"/mnt/sdcard/0001",infor="常量助手")
@log
def reinstalls(deviceId):

    logout(deviceId)
    #登陆
    ui = device.getUiAnazaed(deviceId)
    phoneProduct = device.getPhoneProduct(deviceId)
    login(deviceId, phoneProduct)

@log
def testtt(deviceId):
    ui=device.getUiAnazaed(deviceId)
