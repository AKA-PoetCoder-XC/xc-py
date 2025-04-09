import requests
import pandas_demo
import json
import time
import rsa_util
import concurrent.futures
import pandas as pd

private_key_pem = """-----BEGIN RSA PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEA3JYFhoFtJPR+xoAx
axWcJIzGGuTAN5a2KN4NJVmOd9tRTiGhqkU/XNL0vE6lU5jXgJLVQGOt3P4CJBC6
UhLPjwIDAQABAkEAnS49c7HH/xxFNdbk3+Q/JgA1rbYwjavT010eyu18ykPnixS8
U162zXTQ7AmMe3Y0oJCVehf3wMjNn9GQcErfCQIhAO3d0a3iiv560t40LSYTw8++
mDTVOb4bvUwBPRZzh3d9AiEA7Wb1aSRWvUFuf0lYCKdMrwBUREZcfHMa4k5QUF0z
yPsCIQDAGTcgJee4kvq/JwYbTTUDDlqfuF/Ur1RWEF4ERrLthQIgWj+zt766wsOn
D/h/4PpIqpaDclkVO7I+XB3NZl+oGhUCIQDJc+QHJlkkF0LtkoSqUznF5lpSVRKV
wlyxBHIwk/tzrA==
-----END RSA PRIVATE KEY-----"""

url = "https://openapi.jiayihn.com/api/open/locasys-new-shop/batch-import-point"

# 保存所有导入失败的数据
all_data = []

# 从excel读取数据发送给对应API
def read_excel_import_to_api():
    # 读取excel文件
    excel_data_json = pandas_demo.read_excel()
    # 将数据切割成10个一组
    datalist = split_list_into_chunks(excel_data_json, 10)
    # 使用线程池发送请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futrues = [executor.submit(send_request, data) for data in datalist]
        for future in concurrent.futures.as_completed(futrues):
            # 每个任务的请求结果
            result=future.result()
            if result:
                result_json = json.loads(result)
                if "data" in result_json:
                    all_data.extend(result_json["data"])
    print(f"导入失败的数据：{all_data}")

    # 将all_data转换为DataFrame
    df = pd.DataFrame(all_data)
    
    # 将DataFrame保存为Excel文件
    df.to_excel("导入失败的数据.xlsx", index=False)
    print("数据已保存到导入失败的数据.xlsx")

# 发送请求
def send_request(data):
    current_timestamp = int(time.time() * 1000)
    params = {
        "merchantId": "10004",
        "timeStamp": current_timestamp,
        "params": data
    }
    params_json_string = json.dumps(params, ensure_ascii=False).replace(" ", "") # ensure_ascii=False表示不转换为ascii码，replace(" ", "")表示去掉空格
    print(params_json_string)
    signature=rsa_util.sign_message(private_key_pem, params_json_string.encode())
    params["sign"]=signature
    print(signature)
    response = requests.post(url, json=json.loads(json.dumps(params, ensure_ascii=False).replace(" ", "")), verify=False) # verify=False表示忽略SSL证书验证
    return response.text

# 切割list
def split_list_into_chunks(input_list, chunk_size) -> list:
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

if __name__ == "__main__":
    print("start!")
    # get_token()
    read_excel_import_to_api()