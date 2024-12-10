import socketio
import time

# 创建一个客户端连接
sio = socketio.Client()


# 连接到服务器后触发的事件
@sio.event
def connect():
    print('Connected to server')
    # 发送一条消息给服务器
    sio.send('Hello from client')


# 服务器发送的响应事件
@sio.event
def response(data):
    print('Received from server:', data)
    # 断开连接
    sio.disconnect()


# 服务器发送的消息事件
@sio.event
def message(data):
    print('Received message:', data)


if __name__ == '__main__':
    # 连接到 Flask-SocketIO 服务器
    sio.connect('http://localhost:5000')

    # 等待一些时间以确保测试完成
    time.sleep(2)

    # 关闭客户端连接
    sio.disconnect()
