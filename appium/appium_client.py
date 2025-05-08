import subprocess
import time
import requests

from appium.webdriver.webdriver import WebDriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

from appium_server import AppiumServer

class AppiumClient():

    # 对象成员变量
    app_name:str # app名称，用于模糊匹配
    devices:list = [] # 设备udid列表
    drivers:list = [] # 驱动列表
    app_package:str  # app包名
    app_activity:str # app启动入口
    appium_server:AppiumServer # appium server对象

    def __init__(
        self,
        appium_server:AppiumServer,
        app_name = None,
        devices:list = []
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

        # 初始化设备列表
        if devices:
            self.devices = devices # 指定设备udid列表
        else:
            self.devices = self.get_adb_devices() # 获取连接的设备列表

        # 初始化appium server
        self.appium_server = appium_server # 指定appium server对象

        # 初始化app名称
        if app_name:
            self.app_name = app_name # 指定app名称，用于模糊匹配
            self.app_package = self.get_app_package() # 指定app包名
            self.app_activity = self.get_launch_activity() # 指定app启动入口
            
        # 初始化appium驱动，每个设备对应一个驱动
        self.drivers = self.get_drivers_by_devices()


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
        app_name = self.app_name # 指定app名称
        # 遍历设备列表匹配app名称对应的包名
        for device in self.devices:
            # 使用PowerShell命令(adb -s emulator-5554 shell pm list packages | findstr damai)获取大麦APP的包名
            cmd = ['cmd', '/c', 'adb', '-s', device, 'shell', 'pm', 'list', 'packages', '|', 'findstr', app_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                # 输出格式为 'package:包名'，需要去掉前缀
                app_package = result.stdout.strip().split(':')[1]
                print(f"包名: {app_package}")
                return app_package

        raise ValueError(f"未匹配到包含'{app_name}'的包名!")


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
        app_package:str = self.app_package # 指定app包名
        # 遍历设备列表匹配app包名对应的启动入口
        for device in self.devices:
            # 使用PowerShell命令(adb shell dumpsys package cn.damai | findstr .launcher)获取启动启动入口命令
            cmd = ['cmd', '/c', 'adb', '-s', device, 'shell', 'dumpsys', 'package', app_package, '|', 'findstr', '.launcher']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                # 从输出中提取包含.launcher的Activity名称
                for line in result.stdout.splitlines():
                    if '.launcher' in line:
                        activity = line.split()[1].split('/')[1]
                        print(f"启动Activity: {activity}")
                        return activity
        
        raise ValueError(f"未匹配到包含'{app_package}'的启动入口!")

    
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
        cmd = ['cmd', '/c', 'adb', 'devices']
        result = subprocess.run(cmd, capture_output=True, text=True)
        # 解析设备列表
        for line in result.stdout.splitlines():
            if '\t' in line:
                device = line.split('\t')[0]
                if device != 'List of devices attached':
                    self.devices.append(device)
        if not self.devices:
            raise ValueError('未找到连接的设备!')
        return self.devices


    def get_drivers_by_devices(self) -> list:
        """
        根据设备列表创建驱动列表
        args:
            diveces: 设备udid列表
        return:
            drivers: 驱动列表
        """
        diveces:list = self.devices # 指定设备udid列表
        if not diveces:
            raise ValueError('未找到连接的设备!')
        drivers = []
        # 遍历设备列表构建驱动列表
        for device in self.devices:
            # 获取当前设备对应的Appium server端口
            current_device_server_port = self.appium_server.devices_map_server_port[device]

            # 使用轮询方式检查该端口的Appium server是否已经启动
            max_retry = 10
            retry_count = 0
            retry_interval = 1  # 每次重试间隔1秒
            server_started = False
            
            print(f"等待Appium服务器在端口{current_device_server_port}上启动...")
            while retry_count < max_retry and not server_started:
                try:
                    # 尝试连接服务器，如果成功则跳出循环
                    response = requests.get(f"http://127.0.0.1:{current_device_server_port}/status", timeout=1)
                    if response.status_code == 200:
                        print(f"Appium服务器在端口{current_device_server_port}上已成功启动")
                        server_started = True
                    else:
                        retry_count += 1
                        time.sleep(retry_interval)
                except Exception:
                    retry_count += 1
                    time.sleep(retry_interval)
            
            if not server_started:
                print(f"警告: Appium服务器可能未完全启动，将继续尝试创建会话")
                time.sleep(2)  # 最后再等待2秒
            
            # 初始化Appium驱动
            capabilities = {
                "platform_name": "Android", # 指定设备平台名称
                "device_name": device, # 指定设备名称
                "udid": device,  # 指定设备UDID,可通过adb devices命令查看
                "platform_version": "9",  # 指定Android版本
                # "app_package": self.app_package_name, # 指定启动的app包名
                # "app_activity": self.get_launch_activity(self.app_package_name), # 指定app启动入口，一个app可能有多个入口，需要根据实际情况选择
                "no_reset": "true", # 不重置应用状态
            }
            # 创建Appium驱动对象
            current_device_dirver = WebDriver(command_executor=f"127.0.0.1:{current_device_server_port}", options=UiAutomator2Options().load_capabilities(capabilities))
            current_device_dirver.implicitly_wait(10)
            # 添加驱动对象到驱动列表
            drivers.append(current_device_dirver)
        return drivers
    
    """
    启动app
    author: XieChen
    date: 2025/05/08
    """
    def activate_app(self, appn_package:str):
        # 遍历驱动列表
        for driver in self.drivers:
            # 判断应用是否已经安装
            if not driver.is_app_installed(appn_package):
                raise RuntimeError(f'app{appn_package}未安装,启动失败!')
            # 启动应用
            driver.activate_app(appn_package)
            print(f'app（{appn_package}）已在设备 {driver.capabilities["deviceName"]} 上成功启动')
    
    """
    清除测试环境
    author: XieChen
    date: 2025/05/08
    """
    def close_driver(self):
        for driver in self.drivers:
            if driver:
                driver.quit()


