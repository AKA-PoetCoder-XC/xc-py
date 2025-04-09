# This is a sample Python script.
import sys
import threading


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(name)

def typeTest():
    print(type('str'))

def listTest():
    ls = ['XieChen', 'XiaoTu']
    ls0 = ls[1]
    ls.append("Hello World")
    print(ls)

def tupleTest():
    tps1 = (1, 2, 3)
    tps2 = (4, 5, 6)
    print(id(tps2))
    tp0 = tps1[1]
    tps2 = tps2 * 2
    print(id(tps1))
    print(id(tps2))

def dictTest():
    dict = {}
    dict["name"] = "XieChen"
    dict["age"] = "23"
    dict["name"] = "XiaoTu"
    dict_value1 = dict.setdefault('name', "XieChen")
    del dict["age"]
    print(dict)
    print(dict_value1)

def setTest():
    set1 = set() # 空列表
    set2 = {1}
    set3 = set([1, 2, 3])
    set4 = set((2, 3, 4))
    set1.add("xieChen")
    set1.add("xieMou")
    set1.add("xiaoTu")
    set1.remove("xieChen")
    set1.pop()
    print(set1)
    print(set3.difference(set4))
    set3.difference_update(set4)
    print(set3)
    set3.union(set4)
    print(set3)

def derivationExpressTest():
    new_list = ['Bob', 'Tom', 'alice', 'Jerry', 'Wendy', 'Smith', 1, 2, 3]
    # 筛选列表
    name_list = [item for item in new_list if type(item) == type('str')]
    print(name_list)
    # 列表转字典
    new_dict = {key: len(key) for key in name_list if len(key) > 0}
    print(new_dict)
    # 列表转集合
    set1 = {item for item in name_list if 1 == 1}
    print(set1)
    # 列表转元组生成器
    new_tuple_generator = (item for item in name_list if 1 == 1)
    print(new_tuple_generator)
    new_tuple = tuple(new_tuple_generator)
    print(new_tuple)

def iterTest():
    new_list = ['Bob', 'Tom', 'alice', 1, 2, 3]
    new_iter = iter(new_list)
    # 迭代器输出
    while True:
        try:
            print(next(new_iter), end="\t")
        except StopIteration:
            break
    for i in new_iter:
        print(i, end="\t")

def strTest():
    new_str = "12XieChen231"
    new_str2 = new_str.strip("12")
    print(new_str2)
    print(new_str.count("12"))
    print(new_str[1])

def argTest1(arg):
    print(f"arg: {arg}")

def argTest2(arg1, arg2):
    print(f"arg1: {arg1}, arg2: {arg2}")

def argTest3(arg1, arg2 = "arg2"):
    print(type(arg1), type(arg2))
    print(f"arg1: {arg1}, arg2: {arg2}")

def argTest4(*tuple_args):
    print(type(tuple_args))
    count = 1
    for arg in tuple_args:
        print(f"arg{count}: {arg}")
        count += 1

def argTest5(*tuple_args):
    print(type(tuple_args))
    count = 1
    for arg in tuple_args:
        print(f"arg{count}: {arg}")
        count += 2

def argTest6(**dict_args):
    print(type(dict_args))
    print(dict_args)

def funcTest(*func):
    print(func)
    for func in func:
        result = func(1, 2, 3, 4)
        print(result)

def fileTest():
    fw = open("test.txt", "w", encoding="utf-8")
    fw.write("hello!")
    fw.close()
    fr = open("test.txt", "r", encoding="utf-8")
    print(fr.read())


if __name__ == '__main__':
    # funcTest(argTest4, argTest5)
    # # lamda表达式作为匿名函数传入时函数体只能写一行代码,多行必须用def定义
    # funcTest(lambda x, y, z, h: x+y+z+h)
    fileTest()
