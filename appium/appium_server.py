import subprocess
import socket

class AppiumServer():

    # 对象成员变量
    devices:list = [] # 设备udid列表
    devices_map_appium_server_port:dict = {} # 设备与appium server端口映射关系
    default_port:int = 4723 # 默认端口
    host:str
    def __init__(
        self,
        devices:list = [],
    ):
        """
        对象初始化
        args:
            devices: 设备列表(udid,比如emulator-5554)
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
        return:
            drivers: 驱动列表
        """
        if not self.devices:
            raise ValueError('未找到连接的设备!')
        for index,device in enumerate(self.devices):
            current_device_appium_server_port = AppiumServer.get_port_by_device_index(index)
            # 启动Appium server
            cmd = ['cmd', '/c', 'start', 'appium', '-p', str(current_device_appium_server_port)]
            subprocess.Popen(cmd)
            # 记录设备与appium server端口映射关系
            self.devices_map_appium_server_port[device] = current_device_appium_server_port
            print(f"appium server[{AppiumServer.get_local_ip()}:{current_device_appium_server_port}]启动成功,对应设备[{device}]")

    @staticmethod
    def get_port_by_device_index(device_index:int) -> int:
        """
        获取设备对应的appium server端口
        args:
            device_index: 设备索引
        return:
            port: appium server端口
        """
        return AppiumServer.default_port + device_index

    @staticmethod
    def get_local_ip() -> str:
        """
        获取本机IP地址
        args:
            None
        return:
            ip: 本机IP地址
        """
        try:
            # 创建一个socket连接
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到一个公共DNS服务器（这里使用Google的8.8.8.8）
            s.connect(('8.8.8.8', 80))
            # 获取本机IP地址
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            raise ValueError(f"获取本机IP地址失败: {str(e)}")

if __name__ == '__main__':
    # 启动服务
    appium_server = AppiumServer().start()