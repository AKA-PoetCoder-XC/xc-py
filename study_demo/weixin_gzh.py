import requests
from urllib.parse import quote
import time

def search(search_key:str)->str:
    url="https://mp.weixin.qq.com/cgi-bin/searchbiz"

    headers = {
        "cookie": """slave_user=gh_fecac6d163ff; slave_sid=SDBqN1NZY25ldHAyWUh2SlBIWEJtRFR2MGpLRndHNThpUmR0cW1JbmdHZkYwaG1pTHBKdE5GRU1sNzFrVlNWM1RDNFFSVFpRdmp4MUJzR25NRmZ1SVpacFhTSjJOSUQ1S2plVGNtdlcwMzZBaW1MdVBRSFZRSVV3RGxSVUZqWWR3U2NVMGJvR1FNNXo4TVdX;""",
    }

    params={
        "query": search_key,
        "action": "search_biz",
        "begin": 0,
        "count": 5,
        "fingerprint": "593853ea2a8b8ba08986c004968a5a81",
        "token": "1632687576",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    response = requests.get(url, params=params, headers=headers, verify=False)
    return response.text

if __name__=="__main__":
    data = search("青年湖南")
    print(data)