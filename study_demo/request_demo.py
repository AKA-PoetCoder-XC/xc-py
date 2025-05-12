import requests
import pandas_demo
import json

class LoginUser:
    def __init__(self, userAcct, password):
        self.userAcct = userAcct
        self.password = password

# 获取token
def get_token():
    wmy = LoginUser(userAcct="80000001", password="80000001@0031")
    lf = LoginUser(userAcct="80003602", password="123456")
    hc = LoginUser(userAcct="80000056", password="80000056@1547")
    yj = LoginUser(userAcct="80002254", password="80002254@2071")
    cd= LoginUser(userAcct="80000141", password="80000141@8508")
    loginUser = lf
    url = "https://sso.jiayihn.com/api/auth/oauth2/login"
    params = {
        'userAcct': loginUser.userAcct,
        'password': loginUser.password
    }
    response = requests.post(url, params=params, verify=False) # verify=False表示忽略SSL证书验证
    print(response.text)


if __name__ == "__main__":
    print("start!")

    get_token()