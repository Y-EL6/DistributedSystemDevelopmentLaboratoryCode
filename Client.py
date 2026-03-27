import xmlrpc.client
import time

# ================= 1. 本地调用对比 =================
def add_local(a, b):
    return a + b

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("1. 本地调用测试")
    print("--------------------------------------------------")
    
    # 记录本地调用时间
    start_time_local = time.perf_counter()
    res_local_add = add_local(5, 10)
    end_time_local = time.perf_counter()
    
    print(f"本地调用 add(5, 10) 结果: {res_local_add}")
    print(f"本地调用耗时: {(end_time_local - start_time_local) * 1000:.4f} ms")

    # ================= 2. RPC 远程调用测试 =================
    print("\n--------------------------------------------------")
    print("2. RPC 远程调用测试")
    print("--------------------------------------------------")
    
    # 创建ServerProxy连接到服务端
    proxy = xmlrpc.client.ServerProxy("http://192.168.196.128:8000/")

    try:
        # 记录RPC调用时间
        start_time_rpc = time.perf_counter()
        # 调用远程add方法
        res_rpc_add = proxy.add(5, 10)
        end_time_rpc = time.perf_counter()
        
        print(f"RPC调用 add(5, 10) 结果: {res_rpc_add}")
        print(f"RPC调用耗时: {(end_time_rpc - start_time_rpc) * 1000:.4f} ms")

        print("\n")
        
        # 测试第二个方法
        res_rpc_str = proxy.toUpperCase("hello rpc")
        print(f"RPC调用 toUpperCase('hello rpc') 结果: {res_rpc_str}")

    except ConnectionRefusedError:
        print("RPC调用失败：连接被拒绝。请确认服务端 (server.py) 是否已启动。")
    except Exception as e:
        print(f"RPC调用发生异常: {e}")