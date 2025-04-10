import os
import sys

'''
    统计指定目录及其子目录下所有文件的总行数
    author: XieChen
'''
def count_lines_in_directory(directory="."):
    """计算指定目录及其子目录下所有文件的总行数"""
    total_lines = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = sum(1 for _ in f)
                    total_lines += lines
                    print(f"{file_path}: {lines} 行")
            except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                # 跳过二进制文件、没有权限的文件和目录
                continue
    
    return total_lines

if __name__ == "__main__":
    target_dir = input("请输入要统计的目录路径(留空则统计当前目录): ") or "."
    total = count_lines_in_directory(target_dir)
    print(f"\n总行数: {total} 行")
    
    # 添加等待用户按键的代码
    if sys.platform == 'win32':
        os.system('pause')
    else:
        input("按回车键退出...")