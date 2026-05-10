from xmlrpc.server import SimpleXMLRPCServer

# 1. 定义要暴露的函数
def add(a, b):
    """返回两数之和"""
    return a + b

def toUpperCase(s):
    """将字符串转为大写"""
    return s.upper()

if __name__ == '__main__':
    # 2. 创建SimpleXMLRPCServer实例，监听本地8000端口
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))
    print("RPC 服务端已启动，监听端口 8000...")

    # 3. 注册函数，供客户端通过网络调用
    server.register_function(add, "add")
    server.register_function(toUpperCase, "toUpperCase")

    # 4. 启动服务，持续监听请求
    server.serve_forever()
