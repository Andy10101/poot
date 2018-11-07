from poot.poot import Poot,By
import hashlib,re
m2=hashlib.md5()
m2.update("99000740058334-897590050".encode("utf-8"))
print(m2.hexdigest())
ss='''
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <boolean name="first_launch_weixin" value="false" />
    <int name="default_uin" value="-897590050" />
    <string name="support.weixin.qq.com">szsupport.weixin.qq.com</string>
    <long name="recomended_update_ignore" value="1541164513" />
    <int name="new_launch_image_sub_type" value="100" />
    <boolean name="set_service" value="true" />
    <string name="camera_file_path">/storage/emulated/0/tencent/MicroMsg/WeiXin/microMsg.1517887923978.jpg</string>
    <string name="builtin_short_ips">10,163.177.81.139,80,szshort.weixin.qq.com|18,183.3.224.141,80,szshort.weixin.qq.com|6,121.51.140.139,80,szshort.weixin.qq.com|10,163.177.81.139,80,szextshort.weixin.qq.com|18,183.3.224.141,80,szextshort.weixin.qq.com|6,121.51.140.139,80,szextshort.weixin.qq.com|6,121.51.130.84,80,szshort.pay.weixin.qq.com|6,121.51.140.143,80,szshort.pay.weixin.qq.com|10,163.177.81.143,80,szshort.pay.weixin.qq.com|10,58.251.80.105,80,szshort.pay.weixin.qq.com|18,183.3.224.143,80,szshort.pay.weixin.qq.com|18,183.3.234.104,80,szshort.pay.weixin.qq.com|6,127.0.0.1,80,localhost|</string>
    <int name="launch_last_status" value="2" />
    <int name="appbrand_video_player" value="-1" />
    <long name="new_launch_image_end_time" value="1506589200" />
    <int name="launch_fail_times" value="8" />
    <boolean name="settings_fully_exit" value="false" />
    <long name="new_launch_image_begin_time" value="1506322800" />
    <string name="WHATNEW_REPORT_TIME_STR">2017-12-28</string>
    <long name="NFC_REPORT_TIME" value="1113414497" />
</map>
'''
com=re.compile("_uin\" value=\"(-[\\d]+)\"").findall(ss)[0]
print(com[0])