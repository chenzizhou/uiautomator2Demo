import uiautomator2 as u2
import time
# import pandas as pd
import cv2  # opencv-python
from enum import unique, Enum

SEARCH_PRINTER_EXL_NAME = 'PrinterSearch.xlsx'
AP_NAME = 'Smartisan'
AP_PASSWORD = '11111111'
HW_ACCOUNT = '18501045971'
HW_PASSWORD = 'huawei@p20'
# SCREEN_WIDTH = 1080
# SCREEN_HEIGHT = 2340


APP_SETTING = 'com.android.settings'
APP_PHOTO = 'com.huawei.photos'
APP_GALLERY = 'com.android.gallery3d'


@unique
class WiFiStatus(Enum):
    ''' wifi 状态 '''
    CLOSED, OPENING, CONNECTED = 0, 1, 2


def decor_open_close(func):
    '''装饰 下拉菜单开关 操作'''

    def in_decor(self):
        d = self.u
        d.swipe(0, 0, 0, self.height, 0.1)
        d.swipe(0, 0, 0, self.height, 0.1)
        try:
            succ = func(self)
        except Exception as ex:
            print(str(ex))
        d.swipe(0, self.height, 0, 0, 0.1)
        return succ
        # if d(resourceId="com.android.systemui:id/edit_button").exists():
    return in_decor


class HWDevice(object):
    def __init__(self, sn):
        # cls.u = u2.connect(ip)
        self.u = u2.connect_usb(sn)
        self.u.healthcheck()  # 启动检查
        # hrp = htmlreport.HTMLReport(self.u, 'report')
        # hrp.patch_click()
        img = self.__get_screen_np__()
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.u.implicitly_wait(5.0)
        self.u(resourceId="android:id/button2").click_exists()
        # cls.u.disable_popus(True) # 开启自动处理弹出框
        # cls.u.make_toast('开始测试', 3)
        self.wifi_status = WiFiStatus.CLOSED.value
        self.has_appassword = False

    def dispose(self):
        self.disconnect_wifi(AP_NAME)
        self.close_hwshare()
        # cls.u.make_toast('结束测试', 3)
        # cls.u.app_stop_all()
        # 停止 守护程序
        # cls.u.service('uiautomator').stop()

    def __get_screen_np__(self):
        timestr = time.strftime('%Y_%m%d_%H%M%S')
        img_name = f'img/{timestr}.jpg'
        self.u.screenshot(img_name)
        img = cv2.imread(img_name)
        return img

    def open_screen(self):
        self.u.screen_on()
        self.u.swipe_ext('up')

    def close_screen(self):
        self.u.screen_off()

    def wait_hiplay_device_show(self):
        d = self.u
        d.swipe(10, self.height - 5, 10, 500, 0.1)
        time.sleep(0.5)
        iknow = d(resourceId="android:id/button2")
        if iknow.exists():
            iknow.click()
            d.swipe(10, self.height - 5, 10, 500, 0.1)
        # d.implicitly_wait(10.0)
        exists = False
        for i in range(20):
            time.sleep(1)
            device = d(
                resourceId="com.huawei.controlcenter:id/layout_device_item")
            if device.exists():
                exists = True
                break
        # 关闭窗口
        d.swipe_ext('down')
        return exists

    def wait_hiplay_device_disapare(self):
        d = self.u
        d.swipe(10, self.height - 5, 10, 500, 0.1)
        # d.implicitly_wait(10.0)
        disapare = False
        for i in range(10):
            time.sleep(1)
            device = d(
                resourceId="com.huawei.controlcenter:id/layout_device_item")
            if not device.exists():
                disapare = True
                break
        # 关闭窗口
        d.swipe_ext('down')
        return disapare

    def login(self, account, password):
        with self.u.session(APP_SETTING) as d:
            # d(resourceId="android:id/title", text="登录华为帐号")
            # d.xpath('//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout[2]')
            if d(resourceId="android:id/summary", text="华为帐号、付款与账单、云空间等").exists():
                return
            d.xpath(
                '//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout[2]').click()
            d(resourceId="android:id/button1").click()
            account_el = d(resourceId="com.huawei.hwid:id/email_name")
            account_el.clear_text()
            account_el.send_keys(account)
            password_el = d(resourceId="com.huawei.hwid:id/input_password")
            password_el.clear_text()
            password_el.send_keys(password)
            d(resourceId="com.huawei.hwid:id/btn_login").click()
            d.implicitly_wait(10.0)
            d(resourceId="com.huawei.hidisk:id/uniform_guide_continue_button").click()
            time.sleep(2)
            d(resourceId="android:id/button2").click_exists()
            time.sleep(2)
            d(resourceId="android:id/button2").click_exists()
            return True

    def logout(self):
        with self.u.session(APP_SETTING) as d:
            d.xpath(
                '//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout[2]').click()
            # TODO 可能有紧急联系人添加， 和升级提醒
            d.swipe_ext('up')
            d(resourceId="com.huawei.hwid:id/account_center_logout_btn").click()
            # 退出账号弹窗
            d(resourceId="android:id/button1").click()
            # 退出云空间弹窗
            d(resourceId="android:id/button1").click()
            d(resourceId="com.huawei.hwid:id/input_password").send_keys(HW_PASSWORD)
            d(resourceId="android:id/button1").click()
            time.sleep(2)
            return True

    def __check_color__(self, x, y, color):
        ''' 判断位置颜色是否相符 color:[R,G,B] '''
        img = self.__get_screen_np__()
        px = img[int(y), int(x)]
        c_offset = abs(sum(color) - sum(px))
        return c_offset <= 3

    @decor_open_close
    def open_wifi(self):
        d = self.u
        if d(text="开启", description="WLAN 已开启,,打开WLAN设置。").exists():
            self.wifi_status = WiFiStatus.OPENING.value
            return self.wifi_status
        if d(text="开启", description=f"WLAN 已开启,WLAN 信号强度满格。,{AP_NAME},打开WLAN设置。").exists():
            self.wifi_status = WiFiStatus.CONNECTED.value
            return self.wifi_status
        d(text="关闭", description="WLAN 已关闭,打开WLAN设置。").click()
        self.wifi_status = WiFiStatus.OPENING.value
        time.sleep(3)
        if d(text="开启", description=f"WLAN 已开启,WLAN 信号强度满格。,{AP_NAME},打开WLAN设置。").exists():
            self.wifi_status = WiFiStatus.CONNECTED.value
        return self.wifi_status

    @decor_open_close
    def close_wifi(self):
        d = self.u
        if d(text="关闭", description="WLAN 已关闭,打开WLAN设置。").exists():
            self.wifi_status = WiFiStatus.CLOSED.value
            return
        d(text="开启", description="WLAN 已开启,,打开WLAN设置。").click_exists()
        d(text="开启",
            description=f"WLAN 已开启,WLAN 信号强度满格。,{AP_NAME},打开WLAN设置。").click_exists()
        self.wifi_status = WiFiStatus.CLOSED.value

    def get_wifi_status(self):
        return self.wifi_status

    def connect_wifi(self, apname, appassword):
        self.open_wifi()
        if self.wifi_status == WiFiStatus.CONNECTED.value:
            return True
        with self.u.session(APP_SETTING) as d:
            d.xpath(
                '//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout[3]').click()
            if d(description=f"{apname},已连接 (网络质量好),WLAN 信号强度满格。").exists():
                return True
            d.implicitly_wait(1.0)
            while True:
                ap = d(description=f"{apname},加密,WLAN 信号强度满格。")
                if not ap.exists():
                    self.has_appassword = True
                    self.wifi_status = WiFiStatus.CONNECTED.value
                    d.swipe(self.width - 300, self.height * 0.8,
                            self.width - 300, self.height * 0.6)
                else:
                    break
            ap.click()
            d(resourceId="com.android.settings:id/password").send_keys(appassword)
            d(resourceId="com.android.settings:id/btn_wifi_connect").click()
            time.sleep(4)
            if d(description=f"{apname},已连接 (网络质量好),WLAN 信号强度满格。").exists():
                self.has_appassword = True
                self.wifi_status = WiFiStatus.CONNECTED.value
                return True
            else:
                return False

    def disconnect_wifi(self, apname):
        self.open_wifi()
        with self.u.session(APP_SETTING) as d:
            d.xpath(
                '//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout[3]').click()
            d.implicitly_wait(1.0)
            ap = d(description=f"{apname},已连接 (网络质量好),WLAN 信号强度满格。")
            if not ap.exists():
                return True
            ap.long_click()
            # 不保存网络
            d.xpath(
                '//android.widget.ListView/android.widget.LinearLayout[1]').click()
            self.has_appassword = False
            self.wifi_status = WiFiStatus.OPENING.value
            return True

    @decor_open_close
    def open_ble(self):
        d = self.u
        if d(text="开启", description="蓝牙开启。,未连接。,打开蓝牙设置。").exists():
            return
        d(text="关闭", description="蓝牙关闭。,打开蓝牙设置。").click()

    @decor_open_close
    def close_ble(self):
        d = self.u
        if d(text="关闭", description="蓝牙关闭。,打开蓝牙设置。").exists():
            return
        d(text="开启", description="蓝牙开启。,未连接。,打开蓝牙设置。").click()

    @decor_open_close
    def open_hwshare(self):
        d = self.u
        # if self.__check_color__(837, 346, [254, 125, 0]):
        #     return
        if d(text="开启", description="华为分享").exists():
            return True
        d(text="关闭", description="华为分享").click()
        time.sleep(1)
        d(resourceId="android:id/button1").click_exists()
        # if enshure:
        #     enshure.click()
        d(resourceId="android:id/button1").click_exists()
        # if allowed:
        #     allowed.click()
        return True

    @decor_open_close
    def close_hwshare(self):
        d = self.u
        if d(text="关闭", description="华为分享").exists():
            return True
        d(text="开启", description="华为分享").click()
        time.sleep(2)
        if d(text="关闭", description="华为分享").exists():
            return True
        else:
            return False

    @decor_open_close
    def open_hwshare_pc(self):
        d = self.u
        d(text="开启", description="华为分享").long_click()
        time.sleep(0.5)
        switcher = d.xpath(
            '//*[@resource-id="android:id/list"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
        self.__switch__(switcher, True)

    @decor_open_close
    def close_hwshare_pc(self):
        d = self.u
        d(text="开启", description="华为分享").long_click()
        time.sleep(0.5)
        switcher = d.xpath(
            '//*[@resource-id="android:id/list"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
        self.__switch__(switcher, False)

    def open_hiplay(self):
        with self.u.session(APP_SETTING) as d:
            d(resourceId="android:id/title", text="更多连接").click()
            d.xpath('//*[@resource-id="com.android.settings:id/list"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.TextView[1]').click()
            time.sleep(0.5)
            switcher = d(resourceId="android:id/widget_frame")
            self.__switch__(switcher, True)

    def close_hiplay(self):
        with self.u.session(APP_SETTING) as d:
            d(resourceId="android:id/title", text="更多连接").click()
            d.xpath('//*[@resource-id="com.android.settings:id/list"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.TextView[1]').click()
            switcher = d(resourceId="android:id/widget_frame")
            self.__switch__(switcher, False)

    def open_printservice(self):
        self.__printservice__(True)

    def close_printservice(self):
        self.__printservice__(False)

    def share_photo_to_device(self, device_name):
        photo_name = None
        with self.u.session(APP_PHOTO) as d:
            d.xpath(
                '//*[@content-desc="本地相册"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
            d.xpath(
                '//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]').click()
            photo_name = self.__get_picture_name__()
            d(text="分享").click()
            for i in range(10):
                content = d(
                    resourceId="com.huawei.android.instantshare:id/listview_content_user_list_content")
                child = content.child_by_text(device_name)
                if child.exists():
                    child.click()
                    return True, photo_name
        return False, photo_name

    def receive_share(self):
        d = self.u
        receive = d(resourceId="android:id/button1")
        if receive.exists():
            receive.click()
            time.sleep(2)
            photo_name = self.__get_picture_name__()
            return photo_name

    def __get_picture_name__(self):
        d = self.u
        d(resourceId="com.android.gallery3d:id/head_select_right").click()  # 查看信息
        path_el = d(resourceId="com.android.gallery3d:id/detail_path")
        print(path_el)
        # TODO
        if path_el.exists():
            return path_el.text

    def __printservice__(self, open):
        ''' 切换 打印服务开关 '''
        with self.u.app_start(APP_SETTING, '.Settings$ConnectedDeviceDashboardActivity') as d:
            d.xpath(
                '//*[@resource-id="com.android.settings:id/list"]/android.widget.LinearLayout[7]').click()
            d(resourceId="android:id/summary").click()
            switcher = d(resourceId="android:id/widget_frame")
            self.__switch__(switcher, open)

    def __switch__(self, switcher, open):
        ''' 执行开关操作 '''
        time.sleep(2)  # 等待页面动画执行完成再截图
        if open:
            center = switcher.center()
            x, y = center[0] - 30, center[1]
            if self.__check_color__(x, y, [0, 125, 255]):
                return
            switcher.click()
        else:
            center = switcher.center()
            x, y = center[0] - 30, center[1]
            if self.__check_color__(x, y, [255, 255, 255]):
                return
            switcher.click()

    def __get_share_device_delay__(self, ctrl_name):
        start = time.time()
        self.d(text="分享").click()
        printer = self.d(resourceId="com.huawei.android.instantshare:id/user_title",
                         text=ctrl_name).wait(timeout=15)
        end = time.time()
        if printer:
            return end - start
        else:
            return 0

    # def report_sharedevice_time(self):
    #     d = self.d = self.u.session('com.android.gallery3d')
    #     try:

    #         d.xpath(
    #             '//*[@content-desc="本地相册"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
    #         d.xpath(
    #             '//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]').click()

    #         # 'DIRECT-vR53-TS5100series'
    #         # 'DIRECT-22-HP DeskJet 3630 series'
    #         # 'DIRECT-92-HP DeskJet 5000 series'
    #         devicelist = ['DIRECT-vR53-TS5100series']
    #         dic = {device: [] for device in devicelist}
    #         index = list(range(10))
    #         for i in index:
    #             for device in devicelist:
    #                 delay = self.__get_share_device_delay__(device)
    #                 dic[device].append(delay)
    #                 print('{0}: {1}'.format(device, str(delay)))
    #                 d.press('back')
    #                 time.sleep(2)
    #         index.append('mean')
    #         for k, v in dic.items():
    #             mean = sum(v)/(len(v) - v.count(0))
    #             v.append(mean)
    #         if os.path.exists(SEARCH_PRINTER_EXL_NAME):
    #             os.remove(SEARCH_PRINTER_EXL_NAME)
    #         df = pd.DataFrame(dic, index=index)
    #         df.to_excel(SEARCH_PRINTER_EXL_NAME)
    #     except Exception as ex:
    #         print(str(ex))
    #     finally:
    #         d.close()
