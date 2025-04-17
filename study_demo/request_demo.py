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
    loginUser = wmy
    url = "https://sso.jiayihn.com/api/auth/oauth2/login"
    params = {
        'userAcct': loginUser.userAcct,
        'password': loginUser.password
    }
    response = requests.post(url, params=params, verify=False) # verify=False表示忽略SSL证书验证
    print(response.text)

# 模拟请求
def send_request():
    url = "https://manage.jiayihn.com/api/manage/locasys-point-manage/batch-import-point"
    params = {
        'id': 7989
    }
    headers = {
        'Authorization': 'e5rS9gUDUFSggoHb0Yi0TKR257JtTMMKM1eNp8bY4w1Fvk3xUq7XYPZiangbCZGZo3BjofPnhCsjy1EkK36YB3a6h14whg7fxX78Cw3gBie0acbrkiBQnWKJgS60ucxN'
    }
    
    response = requests.get(url, params=params, headers=headers, verify=False) # verify=False表示忽略SSL证书验证
    print(response.text)

def request_test1():
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5c7bc92d-ba69-45a4-afb9-220176c7195a"
    params = {
    	"msgtype": "text",
    	"text": {
        	"content": "hello world"
    	}
   }
    headers = {
        'Content-Type': 'e5rS9gUDUFSggoHb0Yi0TKR257JtTMMKM1eNp8bY4w1Fvk3xUq7XYPZiangbCZGZo3BjofPnhCsjy1EkK36YB3a6h14whg7fxX78Cw3gBie0acbrkiBQnWKJgS60ucxN'
    }
    
    response = requests.post(url, params=params, headers=headers, verify=False) # verify=False表示忽略SSL证书验证
    print(response.text)

# 本地API测试
def local_api_test():
    url = "http://127.0.0.1:5000/api/post"
    params = {
        "key" : "value"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=params, headers=headers)
    print(response.text)

def read_excel_import_to_api():
    excel_data_json = pandas_demo.read_excel()
    url = "https://manage.jiayihn.com/api/manage/locasys-point-manage/batch-import-point"
    params=excel_data_json
    headers = {
        'Authorization': 'e5rS9gUDUFSggoHb0Yi0TKR257JtTMMKM1eNp8bY4w1Fvk3xUq7XYPZiangbCZGZo3BjofPnhCsjy1EkK36YB3a6h14whg7fxX78Cw3gBie0acbrkiBQnWKJgS60ucxN',
        'Content-Type': 'application/json'
    }
    print(params)    
    response = requests.post(url, json=params, headers=headers, verify=False) # verify=False表示忽略SSL证书验证
    print(response.text)

if __name__ == "__main__":
    print("start!")

    get_token()