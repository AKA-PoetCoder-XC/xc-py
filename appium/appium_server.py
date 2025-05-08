import subprocess

from appium.webdriver.webdriver import WebDriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

class AppiumServer():

    # 对象成员变量
    devices:list = [] # 设备udid列表
    devices_map_server_port:dict = {} # 设备与appium server端口映射关系

    def __init__(
        self,
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

        # 初始化设备列表
        if devices:
            self.devices = devices # 指定设备udid列表
        else:
            self.devices = self.get_adb_devices() # 获取连接的设备列表
        # 启动appium server
        self.start()

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


    def start(self):
        """
        启动appium server
        args:
            diveces: 设备udid列表
        return:
            drivers: 驱动列表
        """
        if not self.devices:
            raise ValueError('未找到连接的设备!')
        port = 4723
        for index,device in enumerate(self.devices):
            current_device_server_port = port + index
            # 启动Appium server
            cmd = ['cmd', '/c', 'start', 'appium', '-p', str(current_device_server_port)]
            subprocess.Popen(cmd)
            # 记录设备与appium server端口映射关系
            self.devices_map_server_port[device] = current_device_server_port
