"""
Python全面知识点示例
包含基础语法、数据结构、函数、面向对象、文件操作等核心知识点
每个知识点都有详细注释和示例
"""

# ========== 1. 基础语法 ==========
def basic_syntax():
    """
    基础语法示例
    包含变量、运算符、类型转换等
    """
    # 变量与数据类型
    integer_var = 10          # 整型
    float_var = 3.14          # 浮点型
    string_var = "Python"     # 字符串
    bool_var = True           # 布尔值
    none_var = None           # 空值
    
    # 类型转换
    str_to_int = int("100")   # 字符串转整型
    int_to_str = str(100)     # 整型转字符串
    
    # 运算符
    arithmetic = 10 + 3 * 2  # 算术运算
    comparison = 10 > 5       # 比较运算
    logical = True and False  # 逻辑运算
    
    # 输出结果
    print(f"整型: {integer_var}, 浮点型: {float_var}")
    print(f"字符串转整型: {str_to_int}, 整型转字符串: {int_to_str}")
    print(f"算术运算结果: {arithmetic}, 比较运算: {comparison}")

# ========== 2. 控制结构 ==========
def control_structures():
    """
    控制结构示例
    包含条件判断和循环结构
    """
    # if-elif-else条件判断
    age = 18
    if age < 13:
        print("儿童")
    elif age < 18:
        print("青少年")
    else:
        print("成年人")
    
    # for循环
    for i in range(5):        # range函数生成序列
        print(f"for循环第{i}次")
    
    # while循环
    count = 0
    while count < 3:
        print(f"while循环第{count}次")
        count += 1            # 计数器递增
    
    # 循环控制
    for i in range(10):
        if i == 2:
            continue          # 跳过本次循环
        if i == 5:
            break             # 终止循环
        print(i)

# ========== 3. 数据结构 ==========
def data_structures():
    """
    数据结构详细示例
    包含列表、元组、字典、集合的完整操作
    """
    # 1. 列表(list) - 可变序列
    print("\n=== 列表操作 ===")
    fruits = ["apple", "banana", "cherry", "date"]
    
    # 基本操作
    fruits.append("elderberry")       # 追加元素
    fruits.insert(1, "blueberry")    # 指定位置插入
    fruits[2] = "blackberry"         # 修改元素
    popped = fruits.pop()            # 移除并返回最后一个元素
    removed = fruits.remove("apple") # 移除指定元素
    
    # 列表切片
    first_two = fruits[:2]           # 前两个元素
    last_two = fruits[-2:]           # 最后两个元素
    every_other = fruits[::2]        # 每隔一个元素
    
    # 列表方法
    fruits_copy = fruits.copy()      # 浅拷贝
    fruits.extend(["fig", "grape"])  # 扩展列表
    index = fruits.index("banana")   # 获取索引
    count = fruits.count("banana")   # 计数
    fruits.sort()                    # 排序(原地修改)
    fruits.reverse()                # 反转(原地修改)
    
    print(f"完整列表: {fruits}")
    print(f"切片示例 - 前两个: {first_two}, 最后两个: {last_two}")
    print(f"列表方法 - 索引: {index}, 计数: {count}")

    # 2. 元组(tuple) - 不可变序列
    print("\n=== 元组操作 ===")
    coordinates = (10, 20, 30)
    single_tuple = (42,)            # 单元素元组必须有逗号
    
    # 元组解包
    x, y, z = coordinates
    first, *rest = coordinates      # 扩展解包
    
    # 元组方法
    index = coordinates.index(20)   # 获取索引
    count = coordinates.count(10)   # 计数
    
    print(f"元组解包: x={x}, y={y}, z={z}")
    print(f"扩展解包: first={first}, rest={rest}")
    print(f"元组方法 - 索引: {index}, 计数: {count}")

    # 3. 字典(dict) - 键值对
    print("\n=== 字典操作 ===")
    person = {
        "name": "Alice",
        "age": 25,
        "city": "Beijing"
    }
    
    # 基本操作
    person["gender"] = "female"     # 添加键值对
    age = person.get("age")         # 安全获取值
    name = person.pop("name")       # 移除并返回值
    keys = person.keys()            # 所有键
    values = person.values()        # 所有值
    items = person.items()         # 所有键值对
    
    # 字典方法
    person_copy = person.copy()     # 浅拷贝
    person.update({"job": "engineer", "age": 26}) # 批量更新
    default = person.setdefault("country", "China") # 设置默认值
    
    print(f"完整字典: {person}")
    print(f"字典视图 - 键: {list(keys)}, 值: {list(values)}")
    print(f"字典方法 - 获取年龄: {age}, 移除的名字: {name}")

    # 4. 集合(set) - 无序不重复
    print("\n=== 集合操作 ===")
    primes = {2, 3, 5, 7}
    evens = {2, 4, 6, 8}
    
    # 基本操作
    primes.add(11)                  # 添加元素
    primes.remove(2)                # 移除元素(不存在会报错)
    primes.discard(3)               # 安全移除(不存在不报错)
    popped = primes.pop()           # 随机移除并返回一个元素
    
    # 集合运算
    union = primes | evens          # 并集
    intersection = primes & evens    # 交集
    difference = primes - evens     # 差集
    symmetric_diff = primes ^ evens  # 对称差集
    
    # 集合方法
    primes.update({11, 13, 17})     # 批量添加
    is_subset = {3, 5}.issubset(primes) # 子集检查
    is_superset = primes.issuperset({5, 7}) # 超集检查
    
    print(f"集合运算 - 并集: {union}, 交集: {intersection}")
    print(f"差集: {difference}, 对称差集: {symmetric_diff}")
    print(f"集合方法 - 子集检查: {is_subset}, 超集检查: {is_superset}")

# ========== 4. 函数 ==========
def function_examples():
    """
    函数示例
    包含参数传递、返回值、作用域等
    """
    # 基本函数定义
    def greet(name):
        """简单的问候函数"""
        return f"Hello, {name}!"
    
    # 默认参数
    def power(num, exponent=2):
        """计算幂次，默认平方"""
        return num ** exponent
    
    # 可变参数
    def sum_numbers(*args):
        """计算任意数量数字的和"""
        return sum(args)
    
    # 关键字参数
    def print_info(**kwargs):
        """打印关键字参数"""
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    
    # lambda表达式
    square = lambda x: x * x
    
    # 函数调用
    print(greet("World"))
    print(power(3))          # 使用默认参数
    print(sum_numbers(1, 2, 3))
    print_info(name="Alice", age=25)
    print(square(5))

# ========== 5. 面向对象 ==========
class Animal:
    """动物基类"""
    
    def __init__(self, name, age):
        """构造函数"""
        self.name = name     # 实例属性
        self.age = age
        self.__secret = "这是私有属性"  # 私有属性
    
    def speak(self):
        """实例方法"""
        return f"{self.name} says hello!"
    
    @classmethod
    def create_baby(cls, name):
        """类方法"""
        return cls(name, age=0)
    
    @staticmethod
    def is_animal():
        """静态方法"""
        return True

class Dog(Animal):
    """Dog类继承自Animal"""
    
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed   # 子类特有属性
    
    def speak(self):
        """重写父类方法"""
        return f"{self.name} barks!"
    
    def fetch(self, item):
        """子类特有方法"""
        return f"{self.name} fetches {item}"

# ========== 6. 文件操作 ==========
def file_operations():
    """文件读写操作示例"""
    
    # 写入文件
    with open("example.txt", "w", encoding="utf-8") as f:
        f.write("Hello, Python!\n")
        f.write("这是第二行内容\n")
    
    # 读取文件
    with open("example.txt", "r", encoding="utf-8") as f:
        content = f.read()   # 读取全部内容
        print("文件内容:")
        print(content)
    
    # 按行读取
    with open("example.txt", "r", encoding="utf-8") as f:
        print("\n按行读取:")
        for line in f:
            print(line.strip())
    
    # 删除文件
    import os
    os.remove("example.txt")

# ========== 7. 异常处理 ==========
def exception_handling():
    """异常处理示例"""
    
    try:
        # 可能引发异常的代码
        result = 10 / 0
    except ZeroDivisionError:
        print("错误: 不能除以零!")
    except Exception as e:
        print(f"发生未知错误: {e}")
    else:
        print("没有发生异常")
    finally:
        print("异常处理完成")

# ========== 8. 高级特性 ==========
def advanced_features():
    """高级特性示例"""
    
    # 列表推导式
    squares = [x**2 for x in range(5)]
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    
    # 字典推导式
    square_dict = {x: x**2 for x in range(5)}
    
    # 生成器表达式
    gen = (x for x in range(100) if x % 3 == 0)
    
    # 装饰器
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print("装饰器: 函数调用前")
            result = func(*args, **kwargs)
            print("装饰器: 函数调用后")
            return result
        return wrapper
    
    @my_decorator
    def say_hello(name):
        print(f"Hello, {name}!")
    
    # 使用示例
    print("列表推导式:", squares)
    print("字典推导式:", square_dict)
    print("生成器前3项:", [next(gen) for _ in range(3)])
    say_hello("Python")

# ========== 主程序 ==========
if __name__ == "__main__":
    print("=== Python知识点演示 ===")
    basic_syntax()
    control_structures()
    data_structures()
    function_examples()
    
    # 面向对象示例
    dog = Dog("Buddy", 3, "Golden Retriever")
    print(dog.speak())
    print(dog.fetch("ball"))
    
    file_operations()
    exception_handling()
    advanced_features()