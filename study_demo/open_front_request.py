import requests
import xjy_rsa_util

# 请求地址,正式环境要改成去掉"dev-"前缀
url_prev = "http://openapi.jiayihn.com/api/open"

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
def push_cockpit_role(point_id):

    # 请求地址
    url = url_prev + "/locasys-new-shop//push-cockpit-role"

    data = {
        "pointId": point_id,
    }
    

    # 构建请求体
    request_body = xjy_rsa_util.build_request_body(
        data = data,
        private_key_pem = private_key_pem,
        merchant_id = merchant_id
    )

    # 打印请求信息
    print(f"url={url}, request_body={request_body}")

    # 发送请求
    response = requests.post(url, json=request_body)

    # 打印响应内容
    print(response.json())

def batch_push_cockpit_role(point_id_list):
    for point_id in point_id_list:
        push_cockpit_role(point_id)



if __name__ == '__main__':
    batch_push_cockpit_role([11685])