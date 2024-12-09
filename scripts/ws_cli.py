import socketio
import json
import asyncio

# 创建 SocketIO 客户端实例
sio = socketio.Client()

# 用于保存收到的响应
response_data = None


# 连接成功事件
@sio.event
async def connect():
    print("Successfully connected to the WebSocket server!")

    # 发送认证信息
    access_token = "your_access_token_here"  # 替换为实际的 access_token
    headers = {
        "access_token": access_token
    }
    await sio.emit("connect", json.dumps({"type": "connect", "headers": headers}))
    print("Authentication data sent. Waiting for server response...")

    # 在发送完数据后，发送一个状态请求或其他操作
    await sio.emit("data", {"request": "status"})  # 示例，发送请求获取状态


# 处理服务器返回的消息
@sio.event
async def message(data):
    print(f"Message received from server: {data}")
    if 'msg' in data:
        if data['msg'] == 'connected to ws server':
            print("Connection successful!")
        else:
            print(f"Server message: {data.get('msg', 'No message provided')}")
    global response_data
    response_data = data  # 保存收到的响应数据


# 处理 `data` 事件，接收从服务器发送的特定数据
@sio.event
async def data(data):
    print(f"Data received from server: {data}")
    global response_data
    response_data = data  # 保存收到的响应数据


# 客户端等待服务器响应的逻辑
async def start_client():
    uri = "http://localhost:5000"  # WebSocket 服务器地址
    try:
        await sio.connect(uri)  # 异步连接到服务器
        print("Waiting for server response...")

        # 等待直到收到服务器的响应
        while response_data is None:  # 等待直到接收到响应
            await asyncio.sleep(1)  # 每1秒检查一次

        print("Received response:", response_data)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        sio.disconnect()  # 断开连接


# 启动客户端
if __name__ == '__main__':
    asyncio.run(start_client())  # 异步运行客户端
