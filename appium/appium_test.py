import subprocess

from appium.webdriver.webdriver import WebDriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

class AppiumTest():

    # 对象成员变量
    app_name:str = "" # app名称，用于模糊匹配
    devices:list = [] # 设备udid列表
    drivers:list = [] # 驱动列表

    def __init__(
        
        self,
        app_name:str,
        devices:list = [],
    ):
        """
        对象初始化
        args:
            app_name: app名称, 用于模糊匹配
            devices: 设备udid列表
        return:
            None
        author: 
            XieChen
        date: 
            2025-05-08
        """
        # 初始化app名称
        if not app_name:
            raise ValueError('app名称不能为空!')
        self.app_name = app_name # 指定app名称，用于模糊匹配

        # 初始化设备列表
        if devices:
            self.devices = devices # 指定设备udid列表
        else:
            self.devices = self.get_adb_devices() # 获取连接的设备列表
        
        # 初始化appium驱动，每个设备对应一个驱动
        self.drivers = self.get_drivers_by_devices(self.devices)

    
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

    def get_drivers_by_devices(self, diveces:list) -> list:
        """
        根据设备列表创建驱动列表
        args:
            diveces: 设备udid列表
        return:
            drivers: 驱动列表
        """
        if not diveces:
            raise ValueError('未找到连接的设备!')
        port = 4723
        drivers = []
        for index,device in self.devices:
            current_device_server_port = port + index
            # 启动Appium server
            cmd = ['cmd', '/c', 'appium', '-p', current_device_server_port]
            subprocess.Popen(cmd)
            capabilities = {
                "platform_name": "Android", # 指定设备平台名称
                "device_name": device, # 指定设备名称
                "udid": device,  # 指定设备UDID,可通过adb devices命令查看
                "platform_version": "9",  # 指定Android版本
                "app_package": self.app_package_name, # 指定启动的app包名
                "app_activity": self.get_launch_activity(self.app_package_name), # 指定app启动入口，一个app可能有多个入口，需要根据实际情况选择
                "no_reset": "true", # 不重置应用状态
            }
            # 创建Appium驱动对象
            current_device_dirver = WebDriver(command_executor=f"127.0.0.1:{current_device_server_port}", options=UiAutomator2Options().load_capabilities(capabilities))
            current_device_dirver.implicitly_wait(10)
            # 添加驱动对象到驱动列表
            drivers.append(current_device_dirver)
        return drivers
    
    def get_app_package(self, app_name:str) -> str:
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
        for device in self.devices:
            # 使用PowerShell命令(adb -s emulator-5554 shell pm list packages | findstr damai)获取大麦APP的包名
            cmd = ['cmd', '/c', 'adb', '-s', device, 'shell', 'pm', 'list', 'packages', '|', 'findstr', app_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                # 输出格式为 'package:包名'，需要去掉前缀
                app_package_name = result.stdout.strip().split(':')[1]
                print(f"包名: {app_package_name}")
                return app_package_name
        raise ValueError(f"未匹配到包含'{app_name}'的包名!")

    """
    根据app包名获取启动入口命令
    author: XieChen
    date: 2025/05/08
    """
    def get_launch_activity(self, app_package_name) -> str:
        for device in self.devices:
            # 使用PowerShell命令(adb shell dumpsys package cn.damai | findstr .launcher)获取启动启动入口命令
            cmd = ['cmd', '/c', 'adb', '-s', device, 'shell', 'dumpsys', 'package', app_package_name, '|', 'findstr', '.launcher']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                # 从输出中提取包含.launcher的Activity名称
                for line in result.stdout.splitlines():
                    if '.launcher' in line:
                        activity = line.split()[1].split('/')[1]
                        print(f"启动Activity: {activity}")
                        return activity
        
        raise ValueError(f"未匹配到包含'{app_package_name}'的启动入口!")

    """
    初始化appium环境
    author: XieChen
    date: 2025/05/08
    """
    def setUp(self):
        # 为每个设备创建一个驱动对象
        for index, device in enumerate(self.devices):
            options = UiAutomator2Options() # 创建UiAutomator2对象，UiAutomator2实现了WebDriver协议对Android设备的支持
            options.platform_name = 'Android' # 指定平台为Android
            options.device_name = device # 指定设备名称
            options.udid = device # 指定设备UDID,可通过adb devices命令查看
            options.platform_version = '9' # 指定Android版本
            # 动态获取APP包名和启动Activity
            self.app_package_name = self.get_app_package(self.app_name)
            options.app_package = self.app_package_name # 指定启动的app包名
            options.app_activity = self.get_launch_activity(self.app_package_name) # 指定app启动入口，一个app可能有多个入口，需要根据实际情况选择
            options.no_reset = True # 不重置应用状态
            # 连接Appium server 并创建驱动对象
            driver = WebDriver(f"http://127.0.0.1:4723", options=options)
            driver.implicitly_wait(10)
            self.drivers.append(driver)
    
    """
    启动app
    author: XieChen
    date: 2025/05/08
    """
    def activate_app(self):
        # 遍历驱动列表
        for driver in self.drivers:
            # 判断应用是否已经安装
            if not driver.is_app_installed(self.app_package_name):
                raise RuntimeError(f'app{self.app_package_name}未安装,启动失败!')
            # 启动应用
            driver.activate_app(self.app_package_name)
            print(f'app（{self.app_package_name}）已在设备 {driver.capabilities["deviceName"]} 上成功启动')
    
    """
    清除测试环境
    author: XieChen
    date: 2025/05/08
    """
    def close_driver(self):
        for driver in self.drivers:
            if driver:
                driver.quit()

if __name__ == '__main__':
    appium_test = AppiumTest(app_name="damai")
    appium_test.activate_app()
    appium_test.close_driver()

