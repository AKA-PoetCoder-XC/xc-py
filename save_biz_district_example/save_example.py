import requests
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import base64
import time


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

def generate_shop_code_by_point_id():
    url = url_prev + "/locasys-new-shop/get-shop-code"

    data = {
        "pointId": 13433
    }

    # 构建请求体
    request_body = build_request_body(
        data=data, private_key_pem=private_key_pem, merchant_id=merchant_id
    )

    # 打印请求信息
    print(f"url={url}, request_body={request_body}")

    # 发送请求
    response = requests.post(url, json=request_body)

    # 打印响应内容
    print(response.json())

'''
推送驾驶舱权限

'''
def push_cockpit_role():
    url = url_prev + "/locasys-new-shop/push-cockpit-role"

    data = {
        "pointId": 418
    }

    # 构建请求体
    request_body = build_request_body(
        data=data, private_key_pem=private_key_pem, merchant_id=merchant_id
    )

    # 打印请求信息
    print(f"url={url}, request_body={request_body}")

    # 发送请求
    response = requests.post(url, json=request_body)

    # 打印响应内容
    print(response.json())

'''
更新商圈例子
'''
def insert_or_update_example():

    # 请求地址
    url = url_prev + "/locasys-new-shop/save-batch-for-open"

    # 构建请求参数(同一district_code中如果存在该business_district_name的非点状商圈则更新不存在则插入，business_district_name_new用于更新原商圈名称)
    data = [
        {
            "business_district_name": "汇景大厦1",
            "business_district_name_new": "汇景大厦",
            "district_code": "430103",
            "location": "112.969029,28.193397;112.96895,28.192156;112.97000781481935,28.19208145606125;112.9702728406143,28.193260896425258;112.969029,28.193397",
        }
    ]

    # 构建请求体
    request_body = build_request_body(
        data=data, private_key_pem=private_key_pem, merchant_id=merchant_id
    )

    # 打印请求信息
    print(f"url={url}, request_body={request_body}")

    # 发送请求
    response = requests.post(url, json=request_body)

    # 打印响应内容
    print(response.json())

"""
根据私钥和字符串生成签名

author: XieChen
data: 2025-04-12
"""


def sign_message_by_private_key(private_key_pem: str, message: bytes) -> str:
    private_key = load_pem_private_key(
        private_key_pem.encode(), password=None, backend=default_backend()
    )
    # 确保是RSA密钥类型
    assert isinstance(private_key, rsa.RSAPrivateKey)
    signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
    return base64.b64encode(signature).decode()


"""
根据请求数据、私钥、商户号生成请求体

author: XieChen
data: 2025-04-12
"""


def build_request_body(
    data,
    private_key_pem: str,
    merchant_id: str,
    timestamp: int = (int(time.time() * 1000)),
):
    # 拼接初始化请求参数
    params = {"merchantId": merchant_id, "timeStamp": timestamp, "params": data}

    # 生成签名
    params_json_str = json.dumps(params, ensure_ascii=False).replace(
        " ", ""
    )  # ensure_ascii=False表示不转换为ascii码，replace(" ", "")表示去掉空格
    signature = sign_message_by_private_key(
        private_key_pem, params_json_str.encode()
    )  # 生成签名

    # 将签名加入请求参数
    params["sign"] = signature

    # 将请求参数转字符串去除空格后转json对象返回
    return json.loads(json.dumps(params, ensure_ascii=False).replace(" ", ""))


"""
校验签名

author: XieChen
data: 2025-04-12
"""


def verify_signature_by_public_key(
    public_key_pem: str, message: bytes, signature: str
) -> bool:
    # 加载公钥
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(), backend=default_backend()
    )

    # 确保是RSA公钥
    assert isinstance(public_key, rsa.RSAPublicKey)

    # 解码签名
    sig_bytes = base64.b64decode(signature)

    try:
        # 验证签名(PKCS1v15填充 + SHA1哈希)
        public_key.verify(sig_bytes, message, padding.PKCS1v15(), hashes.SHA1())
        return True
    except Exception as e:
        print(f"签名验证失败: {str(e)}")
        return False


if __name__ == '__main__':
    push_cockpit_role()
