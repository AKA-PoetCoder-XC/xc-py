import requests
from urllib.parse import quote
import time
import json
import re


ua_id = "ZrEfLEGfJFigy9JfAAAAAGYAiFi6w9-hSjqhP62PsaQ="
wxuin = "45083796618060"
uuid = ""
slave_sid = ""
slave_user = "gh_fecac6d163ff"
token = ""
fingerprint = "ae3d22be88e45b4163f6e29fcb479be4"

def get_ua_id()->str:
    url = "https://mp.weixin.qq.com/"
    response = requests.get(url)
    return get_val_from_cookie(response.headers["Set-Cookie"], "ua_id")


def get_wxuin(
    fingerprint: str = fingerprint,
    ua_id: str = ua_id
):
    url = "https://mp.weixin.qq.com/webpoc/cgi/chat/checkChatPermission"
    headers = {
        "cookie": f"ua_id={ua_id}"
    }
    params = {
        "type": 15,
        "grayType": "random",
        "token": "",
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1,
        "fingerprint": fingerprint,
    }
    response = requests.get(url, headers=headers, params=params)
    return get_val_from_cookie(response.headers["Set-Cookie"], "wxuin")

def get_uuid(
        fingerprint: str = fingerprint,
        ua_id: str = ua_id
):
    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
    headers = {
        "Cookie": f"ua_id={ua_id}; _clck=8a8uld|1|fv7|0; wxuin={wxuin}",
        "referer": "https://mp.weixin.qq.com/"
    }
    params = {
        "userlang": "zh_CN",
        "redirect_url": "",
        "login_type": 3,
        "sessionid": "174513999242135",
        "fingerprint": fingerprint,
        "token": "",
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1
    }
    response = requests.post(url, headers=headers, params=params)
    # print(response.headers)
    return get_val_from_cookie(response.headers["Set-Cookie"], "uuid")





def check_chat_permission():
    url = f"https://mp.weixin.qq.com/webpoc/cgi/chat/checkChatPermission?type=15&grayType=random&token=&lang=zh_CN&f=json&ajax=1&fingerprint={fingerprint}"
    headers = {
        "cookie": f"ua_id={ua_id}"
    }
    response = requests.get(url, headers=headers)
    return response


def login(
    fingerprint: str = fingerprint,
    ua_id: str = ua_id,
    uuid: str = uuid,
    wxuin: str = wxuin
):

    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"

    headers = {
        "Accept": "*/*",
        "Accept-encoding": "gzip, deflate, br, zstd",
        "Accept-language": "zh-CN,zh;q=0.9",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"ua_id={ua_id}; _clck=1fa6up|1|fv8|0; wxuin={wxuin}; uuid={uuid}",
        "Origin": "https://mp.weixin.qq.com",
        "Referer": "https://mp.weixin.qq.com/",
        "Sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "Sec-ch-ua-mobile": "?0",
        "Sec-ch-ua-platform": "\"Windows\"",
        "Sec-fetch-dest": "empty",
        "Sec-fetch-mode": "cors",
        "Sec-fetch-site": "same-origin",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-requested-with": "XMLHttpRequest",
    }

    params = {
        "userlang": "zh_CN",
        "redirect_url": "",
        "cookie_forbidden": 0,
        "cookie_cleaned": 1,
        "plugin_used": 0,
        "login_type": 3,
        "fingerprint": fingerprint,
        "token": "",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    response = requests.post(url, params=params, headers=headers)
    return response


"""
获取重定向地址请求
"""
def redirect(slave_user:str=slave_user, slave_sid:str=slave_sid):
    # 定义目标 URL 和查询参数
    base_url = "https://mp.weixin.qq.com/cgi-bin/loginpage"
    query_params = {
        "url": "/cgi-bin/home?t=home/index&lang=zh_CN"
    }

    # 定义请求头
    headers = {
        "cookie": "slave_sid="+slave_sid+"; slave_user="+slave_user,
    }

    try:
        # 发起 GET 请求
        response = requests.get(base_url, params=query_params, headers=headers, allow_redirects=False)
        return response

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

def search(search_key:str , 
           slave_user:str=slave_user, 
           slave_sid:str=slave_sid, 
           fingerprint:str=fingerprint):

    url="https://mp.weixin.qq.com/cgi-bin/searchbiz"
    
    headers = {
        "cookie": "slave_user="+slave_user+"; slave_sid="+slave_sid,
    }

    params={
        "query": search_key,
        "action": "search_biz",
        "begin": 0,
        "count": 5,
        "fingerprint": fingerprint, # 设备指纹值
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    response = requests.get(url, params=params, headers=headers)
    return response

def get_val_from_cookie(
        cookie_str: str,
        key: str
)->str:

    # 使用正则表达式提取 key 的值
    match = re.search(f"{key}=([^;]+)", cookie_str)
    if match:
        return match.group(1)
    else:
        return ""


if __name__ == "__main__":
    # response = login()
    # response = search("青年湖南")
    ua_id:str=get_ua_id()
    wxuin=get_wxuin()
    uuid=get_uuid()
    response = login(ua_id=ua_id,wxuin=wxuin,uuid=uuid)
    print(f"status_code: {response.status_code}")
    print(f"Request Headers\n: {response.request.headers}")
    print(f"Response Headers\n: {response.headers}")
    print(f"Response Text\n: {response.text}")