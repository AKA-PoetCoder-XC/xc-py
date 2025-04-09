import pandas as pd
import json

def read_excel() -> list:
    # 读取excel文件
    file_path = "C:\\Users\\Administrator\\Documents\\WXWork\\1688857332462035\\Cache\\File\\2025-01\\反馈202501041319未关联点位店号.xlsx"
    df = pd.read_excel(file_path)
    
    # 将所有数字列转换为字符串
    df = df.applymap(lambda x: str(x) if isinstance(x, (int, float)) else x)

    # 将shopCode字段补零到5位
    if 'shopCode' in df.columns:
        df['shopCode'] = df['shopCode'].apply(lambda x: x.zfill(5))
    
    json_data = df.to_json(orient='records', force_ascii=False) # 将读取到的数据转换为json格式
    return json.loads(json_data if json_data else "[]") # 将json格式的数据转换为list格式
    

if __name__ == "__main__":
    print("start!")
    list = read_excel()
    print(type(list))
    # print(type(json.loads(list)))