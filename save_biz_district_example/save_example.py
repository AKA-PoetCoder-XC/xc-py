import requests
import xjy_rsa_util

# 请求地址,正式环境要改成去掉"dev-"前缀
url_prev = "http://dev-openapi.jiayihn.com/api/open"

# 调用方id，由xjy开放平台提供
merchant_id = "10004"

# 调用方私钥，由xjy_rsa_util模块的generate_rsa_keys_pcks8方法生成密钥对，将公钥发给xjy开放平台，私钥由调用方自己保管
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

'''
更新商圈例子
'''
def insert_or_update_example():

    # 请求地址
    url = url_prev + "/locasys-new-shop/save-batch-for-open"

    # 构建请求参数(同一district_code中如果存在该business_district_name的非点状商圈则更新不存在则插入，business_district_name_new用于更新原商圈名称)
    data = [
        {
            "business_district_name": "更新测试商圈1",
            "business_district_name_new": "更新测试商圈1",
            "out_biz_id": "asflhsafhsdfjsahfksajhfksahasdlkfsakfjsha",
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


'''
删除商圈例子
'''
def delete_example():

    # 请求地址
    url = url_prev + "/locasys-new-shop/delete-batch-for-open"
    
    # 构建请求参数
    data = [
        {
            "business_district_name": "测试商圈2",
            "district_code": "430103",
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


if __name__ == '__main__':
    delete_example()