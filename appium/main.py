from appium_client import AppiumClient
from appium_server import AppiumServer


if __name__ == '__main__':
    # 启动appium server
    appium_server = AppiumServer()
    # 实例化appium client并连接appium server
    appium_client = AppiumClient(appium_server)
    # 启动app
    appium_client.activate_app("cn.damai")
    
    # 关闭appium client
    appium_client.close_driver()