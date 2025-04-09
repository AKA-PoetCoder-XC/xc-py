import json

def dumps_demo():
    data = {
        "name": "张三",
        "age": 18,
        "gender": "男"
    }
    json_str = json.dumps(data, ensure_ascii=False)
    print(type(json_str))
    print(json_str)

def loads_demo():
    dict_json_str = '{"name": "张三", "age": 18, "gender": "男"}'
    list_json_str = '[{"name": "张三", "age": 18, "gender": "男"}, {"name": "李四", "age": 19, "gender": "男"}]'
    list_obj = json.loads(dict_json_str)
    dict_obj = json.loads(list_json_str)
    print(type(list_obj))
    print(type(dict_obj))

if __name__ == "__main__":
    loads_demo()