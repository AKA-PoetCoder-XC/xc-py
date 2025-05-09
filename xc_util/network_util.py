import socket

def get_local_ip() -> str:
    """
    获取本机IP地址
    args:
        None
    return:
        ip: 本机IP地址
    """
    try:
        # 创建一个socket连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共DNS服务器（这里使用Google的8.8.8.8）
        s.connect(('8.8.8.8', 80))
        # 获取本机IP地址
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"获取本机IP失败: {e}")
        return "127.0.0.1"

if __name__ == '__main__':
    print(f"本机IP地址: {get_local_ip()}")