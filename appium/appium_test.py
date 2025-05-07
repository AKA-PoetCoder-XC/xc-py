import unittest
import subprocess
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

class TestDamai(unittest.TestCase):
    @staticmethod
    def get_app_package():
        # 使用PowerShell命令(adb shell pm list)获取大麦APP的包名
        cmd = ['adb', 'shell', 'pm', 'list', 'packages', '|', 'Select-String', 'damai']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout.strip():
            # 输出格式为 'package:包名'，需要去掉前缀
            return result.stdout.strip().split(':')[1]
        return 'cn.damai'  # 默认包名
    
    @staticmethod
    def get_launch_activity():
        # 使用PowerShell命令(adb shell dumpsys package cn.damai)获取启动Activity
        cmd = ['adb', 'shell', 'dumpsys', 'package', 'cn.damai', '|', 'Select-String', 'android.intent.action.MAIN']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return '.launcher.splash.SplashMainActivity'  # 默认启动Activity

    def setUp(self):
        # 设置Appium的Options
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = 'emulator-5554'
        options.platform_version = '9'  # 根据实际Android版本修改
        # 动态获取APP包名和启动Activity
        options.app_package = self.get_app_package()  # 获取大麦APP的包名
        options.app_activity = self.get_launch_activity()  # 获取启动Activity
        options.no_reset = True  # 保留应用数据和登录状态
        # 连接Appium服务器
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)
        self.driver.implicitly_wait(10)
    
    def test_launch_app(self):
        # 验证应用是否成功启动
        app_package = self.get_app_package()
        self.assertTrue(self.driver.is_app_installed(app_package))
        print(f'大麦APP（{app_package}）已成功启动')
        
    def test_app_info(self):
        # 测试获取APP信息的方法
        package = self.get_app_package()
        activity = self.get_launch_activity()
        print(f'获取到的APP包名: {package}')
        print(f'获取到的启动Activity: {activity}')
    
    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()
