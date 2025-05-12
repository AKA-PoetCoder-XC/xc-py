"""
此模块提供了Appium服务器的管理功能

主要功能包括:
- 启动和管理多个Appium服务器实例
- 自动分配端口号
- 管理设备与服务器端口的映射关系
- 获取本地IP地址

作者: XieChen
日期: 2025-05-08
"""
import subprocess
import socket


class AppiumServer:
    """
    Appium服务器管理类

    该类用于管理多个Appium服务器实例,提供以下功能:
    - 自动获取和管理连接的Android设备
    - 为每个设备启动独立的Appium服务器
    - 自动分配服务器端口
    - 维护设备与服务器端口的映射关系
    - 获取本地IP地址用于服务器配置

    属性:
        devices (list): 设备udid列表
        devices_map_appium_server_port (dict): 设备与appium server端口映射关系
        default_port (int): 默认起始端口号(4723)
        host (str): 服务器主机地址
    """

    # 对象成员变量
    devices: list = []  # 设备udid列表
    devices_map_appium_server_port: dict = {}  # 设备与appium server端口映射关系
    default_port: int = 4723  # 默认端口
    host: str

    def __init__(
        self,
        devices: list = None,
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
            self.devices = devices  # 指定设备udid列表
        else:
            self.devices = self.get_adb_devices()  # 获取连接的设备列表

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

    def start(self):
        """
        启动appium server
        return:
            drivers: 驱动列表
        """
        if not self.devices:
            raise ValueError("未找到连接的设备!")
        for index, device in enumerate(self.devices):
            current_device_appium_server_port = AppiumServer.get_port_by_device_index(
                index
            )
            # 启动Appium server
            cmd = [
                "cmd",
                "/c",
                "start",
                "appium",
                "-p",
                str(current_device_appium_server_port),
            ]
            subprocess.Popen(cmd)
            # 记录设备与appium server端口映射关系
            self.devices_map_appium_server_port[device] = (
                current_device_appium_server_port
            )
            print(
                f"""appium server[{AppiumServer.get_local_ip()}:{current_device_appium_server_port}]
                启动成功,对应设备[{device}]"""
            )

    @staticmethod
    def get_port_by_device_index(device_index: int) -> int:
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
            s.connect(("8.8.8.8", 80))
            # 获取本机IP地址
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            raise ValueError(f"获取本机IP地址失败: {str(e)}") from e


if __name__ == "__main__":
    # 启动服务
    AppiumServer().start()
