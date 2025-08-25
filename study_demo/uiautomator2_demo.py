"""
uiautomator2 自动化测试工具模块
用于Android设备的UI自动化测试,提供设备连接和控制功能
"""
import uiautomator2 as u2

d = u2.connect()  # connect to device
print(d.info)
