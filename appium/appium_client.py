"""
Appium客户端模块，用于管理Appium会话和设备交互。

该模块提供了AppiumClient类，用于:
- 管理与Android设备的连接
- 启动和控制Appium会话
- 执行应用程序自动化操作
- 处理多设备并行测试场景

主要功能:
- 自动检测和连接Android设备
- 管理Appium服务器连接
- 提供应用程序操作接口
- 支持多设备并行测试

作者: XieChen
日期: 2025-05-08
"""

from concurrent.futures import ThreadPoolExecutor
import subprocess
import time
import os
import requests
from appium_server import AppiumServer
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class AppiumClient:
    """
    Appium客户端类用于管理Appium会话和设备交互。

    主要功能:
    - 管理与Android设备的连接
    - 启动和控制Appium会话
    - 执行应用程序自动化操作
    - 处理多设备并行测试场景

    属性:
        app_name (str): app名称,用于模糊匹配
        devices (list): 设备udid列表
        drivers (list): 驱动列表
        app_package (str): app包名
        app_activity (str): app启动入口
        appium_server_host (str): appium server主机地址
        devices_map_appium_server_port (dict): device与appium server端口映射关系
    """

    # 对象成员变量
    app_name: str  # app名称，用于模糊匹配
    devices: list = []  # 设备udid列表
    drivers: list = []  # 驱动列表
    app_package: str  # app包名
    app_activity: str  # app启动入口
    app_apk_path: str  # app apk路径
    appium_server_host: str  # appium server主机地址，默认为本地
    devices_map_appium_server_port: dict = {}  # device与appium server端口映射关系
    time_for_wait_element: int = 10  # 等待元素出现的时间

    def __init__(
        self,
        appium_server=None,
        app_name: str = None,
        devices: list = None,
        appium_server_host: str = "127.0.0.1",
        time_for_wait_element: int = None,
    ):
        """
        对象初始化
        args:
            app_name: app名称, 用于模糊匹配
            appium_server: appium server对象
            devices: 设备udid列表
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        # 指定appium server主机地址
        if appium_server_host:
            self.appium_server_host = appium_server_host
        else:
            self.appium_server_host = "127.0.0.1"

        # 初始化设备列表
        if devices:
            self.devices = devices  # 指定设备udid列表
        else:
            self.devices = self.get_adb_devices()  # 获取连接的设备列表

        # 初始化appium server
        if not appium_server and isinstance(appium_server, AppiumServer):
            self.devices_map_server_port = (
                appium_server.devices_map_appium_server_port
            )  # 指定appium server对象
            self.appium_server_host = appium_server.host  # 指定appium server主机地址

        # 初始化app名称
        if app_name:
            self.app_name = app_name  # 指定app名称，用于模糊匹配
            self.app_package = self.get_app_package()  # 指定app包名
            self.app_activity = self.get_launch_activity()  # 指定app启动入口

        # 连接appium_server并获取驱动，每个设备对应一个驱动
        self.drivers = self.connect_to_server()

        # 指定等待元素出现的时间
        if time_for_wait_element:
            self.time_for_wait_element = time_for_wait_element  # 指定等待元素出现的时间

    def get_app_package(self) -> str:
        """
        根据app名称获取app包名
        args:
            app_name: app名称
        return:
            app_package_name: app包名
        author:
            XieChen
        date:
            2025-05-08
        """
        app_name = self.app_name  # 指定app名称
        # 遍历设备列表匹配app名称对应的包名
        for device in self.devices:
            # 使用PowerShell命令(adb -s emulator-5554 shell pm list packages | findstr damai)获取大麦APP的包名
            cmd = [
                "cmd",
                "/c",
                "adb",
                "-s",
                device,
                "shell",
                "pm",
                "list",
                "packages",
                "|",
                "findstr",
                app_name,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout.strip():
                # 输出格式为 'package:包名'，需要去掉前缀
                app_package = result.stdout.strip().split(":")[1]
                print(f"包名: {app_package}")
                return app_package

        raise ValueError(f"未匹配到包含app_name['{app_name}']的包名!")

    def get_launch_activity(self) -> str:
        """
        根据app包名获取启动入口
        args:
            app_package: app包名
        return:
            app_activity: app启动入口
        author:
            XieChen
        date:
            2025-05-08
        """
        app_package: str = self.app_package  # 指定app包名
        # 遍历设备列表匹配app包名对应的启动入口
        for device in self.devices:
            # 使用PowerShell命令(adb shell dumpsys package cn.damai | findstr .launcher)获取启动启动入口命令
            cmd = [
                "cmd",
                "/c",
                "adb",
                "-s",
                device,
                "shell",
                "dumpsys",
                "package",
                app_package,
                "|",
                "findstr",
                ".launcher",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout.strip():
                # 从输出中提取包含.launcher的Activity名称
                for line in result.stdout.splitlines():
                    if ".launcher" in line:
                        activity = line.split()[1].split("/")[1]
                        print(f"启动Activity: {activity}")
                        return activity

        raise ValueError(f"未匹配到包含'app_package[{app_package}]'的启动入口!")

    def get_adb_devices(self) -> list:
        """
        获取adb连接的设备列表
        args:
            None
        return:
            devices: 设备udid列表
        author:
            XieChen
        date:
            2025-05-08
        """
        # 使用命令(adb devices)获取连接的设备列表
        cmd = ["cmd", "/c", "adb", "devices"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # 解析设备列表
        for line in result.stdout.splitlines():
            if "\t" in line:
                parts = line.split("\t")
                device = parts[0]
                status = parts[1] if len(parts) > 1 else ""
                if device != "List of devices attached" and status == "device":
                    self.devices.append(device)
        if not self.devices:
            raise ValueError("未找到连接的设备!")
        return self.devices

    def connect_to_server(self) -> list:
        """
        根据设备列表创建驱动列表
        args:
            diveces: 设备udid列表
        return:
            drivers: 驱动列表
        """
        host = self.appium_server_host
        diveces: list = self.devices  # 指定设备udid列表
        if not diveces:
            raise ValueError("未找到连接的设备!")
        drivers = []
        # 遍历设备列表构建驱动列表
        for index, device in enumerate(self.devices):
            # 从设备对应appium端口获取当前设备对应的Appium server端口
            if self.devices_map_appium_server_port:
                current_device_appium_server_port = self.devices_map_server_port[device]
            else:
                # 未指定appium server端口，使用默认端口4723
                current_device_appium_server_port = (
                    AppiumServer.get_port_by_device_index(index)
                )

            # 使用轮询方式检查该端口的Appium server是否已经启动
            max_retry = 10
            retry_count = 0
            retry_interval = 1  # 每次重试间隔1秒
            server_started = False

            while retry_count < max_retry and not server_started:
                try:
                    print(
                        f"""device[{device}]等待app server
                        在[{host}:{current_device_appium_server_port}]上启动..."""
                    )
                    # 尝试连接服务器，如果成功则跳出循环
                    response = requests.get(
                        f"http://{host}:{current_device_appium_server_port}/status",
                        timeout=1,
                    )
                    if response.status_code == 200:
                        server_started = True
                    else:
                        retry_count += 1
                        time.sleep(retry_interval)
                except Exception as e:
                    print(f"连接Appium server异常: {e}")
                    retry_count += 1
                    time.sleep(retry_interval)

            if not server_started:
                print(
                    f"警告:device[{device}]对应的appium server可能未完全启动,将继续尝试连接..."
                )
                time.sleep(2)  # 最后再等待2秒

            # 初始化Appium驱动
            capabilities = {
                "platform_name": "Android",  # 指定设备平台名称
                "device_name": device,  # 指定设备名称
                "udid": device,  # 指定设备UDID,可通过adb devices命令查看
                "platform_version": "9",  # 指定Android版本
                # "app_package": self.app_package_name, # 指定启动的app包名
                # "app_activity": self.get_launch_activity(self.app_package_name), # 指定app启动入口，一个app可能有多个入口，需要根据实际情况选择
                "no_reset": "true",  # 不重置应用状态
                "waitForIdleTimeout": 0,  # 控制Appium在操作后等待应用进入空闲状态的时间（毫秒）,
            }
            # 创建Appium驱动对象
            current_device_dirver = webdriver.Remote(
                command_executor=f"127.0.0.1:{current_device_appium_server_port}",
                options=UiAutomator2Options().load_capabilities(capabilities),
            )
            current_device_dirver.implicitly_wait(
                self.time_for_wait_element
            )  # 元素出现之前的等待时间设置
            # 添加驱动对象到驱动列表
            drivers.append(current_device_dirver)
            print(
                f"device[{device}]成功连接到Appium server, 端口号:[{current_device_appium_server_port}]"
            )
        return drivers

    def activate_app(self, appn_package: str, app_apk_path: str = None):
        """
        启动app
        args:
            appn_package: app包名
            app_apk_path: app apk路径(如果未安装)
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """

        def _activate_app(driver):
            # 判断应用是否已经安装
            if not driver.is_app_installed(appn_package):
                if app_apk_path:
                    # 安装应用
                    print(f"app[{appn_package}]未安装,正在尝试安装...")
                    os.system(
                        f"adb -s {driver.capabilities['udid']} install {app_apk_path}"
                    )
                    print(f"app[{appn_package}]已成功安装!")
                else:
                    raise ValueError(
                        f"app[{appn_package}]未安装,请指定app_apk_path参数!"
                    )

            # 启动应用
            driver.activate_app(appn_package)
            print(
                f'app[{appn_package}]已在设备[{driver.capabilities["deviceName"]}]上成功启动'
            )

        # 使用线程池并行执行
        with ThreadPoolExecutor() as executor:
            executor.map(_activate_app, self.drivers)

    def close_driver(self):
        """
        关闭驱动连接
        args:
            None
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        for driver in self.drivers:
            if driver:
                driver.quit()

    def process(self):
        """
        开始对应用进行操作
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """

        for driver in self.drivers:

            # # 初始化app服务协议点击“同意”
            # start_time = time.time()
            # try:
            #     driver.find_elements(
            #         by=AppiumBy.ID, value="cn.damai:id/id_boot_action_agree"
            #     )[0].click()
            #     print("点击“同意”成功!")
            # except Exception as e:
            #     print(f"点击“同意”失败!: {e}")

            # # 广告点击跳过
            # start_time = time.time()
            # try:
            #     driver.find_elements(by=AppiumBy.ID, value="cn.damai:id/skip")[
            #         0
            #     ].click()
            #     print(f"广告点击“跳过”耗时: {time.time() - start_time:.2f}秒")
            # except Exception as e:
            #     print(f"广告点击“跳过”失败!: {e}")

            # # 定位底部“我的”元素进行点击
            # self.click_mine(driver)

            # # 点击“立即登录"
            # self.login_now(driver)

            # # 勾选阅读并同意协议
            # self.read_and_accept(driver)

            # # 点击“淘宝登录”
            # self.login_by_taobao(driver, "18873959885")

            # 打开"想看"列表
            self.open_want_to_see_list(driver)

            # 点击第一个想看的演出
            self.click_first_want_to_see_performance(driver)

    def click_first_want_to_see_performance(self, driver):
        """
        点击第一个想看的演出
        args:
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        start_time = time.time()
        try:
            driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,('text("购票")'))[0].click()
            print(f"点击“第一个想看的演出”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“第一个想看的演出”失败!: {e}")

    def open_want_to_see_list(self, driver):
        """
        打开“想看”列表
        args:
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        start_time = time.time()
        try:
            driver.find_elements(by=AppiumBy.ID, value="cn.damai:id/tv_mine_want")[
                0
            ].click()
            print(f"点击“想看”列表耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“想看”列表失败!: {e}")

    def click_mine(self, driver):
        """
        点击“我的”
        args:
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        start_time = time.time()
        try:
            driver.find_elements(by=AppiumBy.ID, value="cn.damai:id/tab_text")[
                4
            ].click()
            print(f"点击“我的”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“我的”失败!: {e}")

    def login_now(self, driver):
        """
        点击“立即登录”
        args:
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        start_time = time.time()
        try:
            driver.find_elements(
                by=AppiumBy.ID, value="cn.damai:id/mine_center_header_user_name"
            )[0].click()
            print(f"点击“立即登录”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“立即登录”失败!: {e}")

    def read_and_accept(self, driver):
        """
        点击“阅读并同意”
        args:
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        start_time = time.time()
        try:
            # 点击“阅读并同意”
            driver.find_elements(by=AppiumBy.ID, value="android.widget.TextView")[
                0
            ].click()
            print(f"点击“阅读并同意”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“阅读并同意”失败!: {e}")


    def login_by_taobao(self, driver, phone: str):
        """
        淘宝登录
        args:
            phone: 手机号
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        # 点击“淘宝登录”
        start_time = time.time()
        try:
            driver.find_elements(
                by=AppiumBy.ID, value="cn.damai:id/login_third_tb_btn"
            )[0].click()
            print(f"点击“淘宝登录”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“淘宝登录”失败!: {e}")
        # 点击短信验证码登录
        start_time = time.time()
        try:
            driver.find_elements(
                by=AppiumBy.ACCESSIBILITY_ID, value="短信验证码登录"
            )[0].click()
            print(f"点击“短信验证码登录”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“短信验证码登录”失败!: {e}")
        # 输入手机号
        start_time = time.time()
        try:
            driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR, ('text("请输入手机号")')
            )[0].click()
            print(f"输入手机号耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"输入手机号失败!: {e}")
        


    def login_by_phone(self, driver, phone: str):
        """
        手机号登录
        args:
            phone: 手机号
            driver: appium driver
        return:
            None
        author:
            XieChen
        date:
            2025-05-08
        """
        # 点击“手机号登录”
        start_time = time.time()
        try:
            driver.find_elements(
                by=AppiumBy.ID, value="cn.damai:id/login_third_account_btn"
            )[0].click()
            print(f"点击“手机号登录”耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"点击“手机号登录”失败!: {e}")
        # 登录
        start_time = time.time()
        try:
            # 输入手机号
            driver.find_elements(
                by=AppiumBy.ID, value="cn.damai:id/aliuser_login_mobile_et"
            )[0].send_keys(phone)
            print(f"输入手机号耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"输入手机号失败!: {e}")
        
        # # 登录
        # start_time = time.time()
        # try:
        #     # 输入手机号
        #     driver.find_elements(
        #         by=AppiumBy.ID, value="cn.damai:id/aliuser_login_mobile_et"
        #     )[0].send_keys(phone)
        #     print(f"输入手机号耗时: {time.time() - start_time:.2f}秒")
        # except Exception as e:
        #     print(f"输入手机号失败!: {e}")


if __name__ == "__main__":
    # 实例化appium client并连接appium server
    appium_client = AppiumClient(appium_server_host="127.0.0.1")
    # # 启动app
    # appium_client.activate_app("cn.damai", app_apk_path="F:\\damai.apk")
    # 开始对应用进行操作
    # appium_client.process()
    # appium_client.login_by_taobao(appium_client.drivers[0], "18873959885")

    # 关闭appium client
    appium_client.process()
