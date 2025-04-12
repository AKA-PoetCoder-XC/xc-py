import requests
import xjy_rsa_util

# 请求地址,正式环境要改成去掉"dev-"前缀
url = "http://dev-openapi.jiayihn.com/api/open/locasys-new-shop/save-batch-for-open"

# 调用方id，由xjy开放平台提供
merchant_id = "10004"

# 调用方私钥
private_key_pem = """-----BEGIN PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEA3JYFhoFtJPR+xoAx
axWcJIzGGuTAN5a2KN4NJVmOd9tRTiGhqkU/XNL0vE6lU5jXgJLVQGOt3P4CJBC6
UhLPjwIDAQABAkEAnS49c7HH/xxFNdbk3+Q/JgA1rbYwjavT010eyu18ykPnixS8
U162zXTQ7AmMe3Y0oJCVehf3wMjNn9GQcErfCQIhAO3d0a3iiv560t40LSYTw8++
mDTVOb4bvUwBPRZzh3d9AiEA7Wb1aSRWvUFuf0lYCKdMrwBUREZcfHMa4k5QUF0z
yPsCIQDAGTcgJee4kvq/JwYbTTUDDlqfuF/Ur1RWEF4ERrLthQIgWj+zt766wsOn
D/h/4PpIqpaDclkVO7I+XB3NZl+oGhUCIQDJc+QHJlkkF0LtkoSqUznF5lpSVRKV
wlyxBHIwk/tzrA==
-----END PRIVATE KEY-----"""

if __name__ == '__main__':

    private_key_pem = """-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBANWW2pMa7p2RipDr
h0Nyql4qikaMCyjpl/MBiR7zTdRGV1d3ce0fcW3yi1hlu3NAgyxPT42YT+IbWFm3
PWyBFH6vcYHWJfTKBqyQSJkOVnS3BPaPirR2NvBAujXtbiuYVwHf8/1pl74nihjU
tBWWjY2FbG0jwikCAK3+o1xryjLLAgMBAAECgYAtbZdxoFHOG62AI0gytUm9G4kr
dg/NlNlnqxTyC0erdYaQKOyHRZ/HhcXTeFfFLJx5qSi/cfzTl4NUGaAr2sxzvf63
ZFbXr7LIOVDCO263MfqLmHCN2KxC8pdNrBj62jmnzHaNUTDvP3wE7QzsFSDoCK3A
va2DicuKRgX3lZu8kQJBAOoglrEvNuaO/eR2gU3vO9MJ3EyjclV76LUSK6f6V2gk
zhWgQfOySihQmCsAQcbU2rO7qDkvonW+dRFM6aJSiwMCQQDpixNh+HMFFiljpMZC
YOSUPdn7RjQz1DdDLjvVQzc2aaqYmsZkkqJKD2HmJZnGVjfsV9WobsN2G7CWgARq
rQqZAkB17hJZj3G08qO6l2KMUgutQpM/2zh1DKPryQpKY1PxtlBEHmP6D31BD0+G
oWuAbqj2zXhvzamka1nma/pm8/LnAkEA0MfAACl3yehR//5iLx0nu06//F56dIsX
DDvcyX5ZcY9tLxfOnEJqSwMNZg3fNuwE+ohbPUQoAQIoD6NKT4N6oQJBAIsBC2YP
Tfcr0PInlzSU/QaseHymOPRxatTR+xzQEonEklZc5tQoKmAtUlNtPSjkm9wsr3ma
R/+jD/0p7JZ9D10=
-----END PRIVATE KEY-----"""

    # 构建请求参数
    data = [
        {
            "business_district_name": "测试商圈1",
            "district_code": "430103",
            "location": "112.969029,28.193397;112.96895,28.192156;112.970008,28.192081;112.970273,28.193261;112.969029,28.193397",
            "passenger_flow": "10000",
            "unint_passenger_flow": "5000.5",
            "level": "S"
        },
        {
            "business_district_name": "测试商圈2",
            "district_code": "430103",
            "location": "112.976346,28.186487;112.976348,28.183704;112.979951,28.183463;112.980165,28.185817;112.979006,28.185817;112.978126,28.185999;112.976501,28.186639;112.976346,28.186487",
            "passenger_flow": "5000",
            "unint_passenger_flow": "500.5",
            "level": "A"
        }
    ]

    # 下划线转驼峰
    camel_data = [
        {
            xjy_rsa_util.underscore_to_camel(k): v
            for k, v in item.items() # 遍历每个字典对象的键值对
        }
        for item in data # 遍历列表中的每个字典对象
    ]

    # 构建请求体
    request_body = xjy_rsa_util.build_request_body(
        data = camel_data,
        private_key_pem = private_key_pem,
        merchant_id = merchant_id
    )

    # 打印请求信息
    print(f"url={url}, request_body={request_body}")

    # 发送请求
    response = requests.post(url, json=request_body)

    # 打印响应内容
    print(response.json())