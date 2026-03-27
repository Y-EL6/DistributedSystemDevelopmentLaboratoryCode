import xmlrpc.client
import time
import socket

# 【新增】设置全局 Socket 超时时间为 3 秒，防止网络阻塞导致客户端一直死等
socket.setdefaulttimeout(3.0)

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

    # ================= 3. 模拟网络故障与重试 (扩展部分) =================
    print("\n--------------------------------------------------")
    print("3. 模拟网络故障与重试机制测试")
    print("--------------------------------------------------")
    
    max_retries = 5       # 最大重试次数
    retry_delay = 3       # 每次重试间隔的秒数
    
    print("💡 准备进行断网测试...")
    print("👉 请在接下来的 5 秒内，切换到服务端终端，按下 【Ctrl + C】 关闭服务端进程！")
    time.sleep(5) # 预留5秒钟让你去关闭服务端
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"▶️ [第 {attempt} 次尝试] 正在发起 RPC 调用 add(100, 200)...")
            # 尝试远程调用
            res_retry = proxy.add(100, 200)
            
            # 如果上面这行没有报错，说明调用成功（网络正常或已恢复）
            print(f"✅ 调用成功: 100 + 200 = {res_retry}")
            break # 成功则跳出循环，不再重试
            
        except ConnectionRefusedError:
            print(f"❌ 尝试 {attempt} 失败：连接被拒绝 (网络已断开或服务端未启动)。")
        except socket.timeout:
            print(f"❌ 尝试 {attempt} 失败：请求超时 (服务端无响应)。")
        except Exception as e:
            print(f"❌ 尝试 {attempt} 失败：发生其他异常 ({e})。")
        
        # 如果还没达到最大重试次数，则等待后继续
        if attempt < max_retries:
            print(f"⏳ 等待 {retry_delay} 秒后重试... (此时你可以尝试重新启动服务端 `python Server.py`)\n")
            time.sleep(retry_delay)
    else:
        # for循环正常结束（没有被break打断），说明所有重试都用光了
        print(f"🚨 已达到最大重试次数 ({max_retries} 次)，RPC 调用彻底失败。")