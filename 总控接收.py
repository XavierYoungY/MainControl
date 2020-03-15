from socket import *
import json


computer1={
    'IP_list':["192.168.1.101","192.168.1.102","192.168.1.103"],
    'port':9000,
    "function": "objectDetection",
    'des_ip':'127.0.0.1'
}

computer2 = {
    'IP_list': ["192.168.1.104", "192.168.1.105", "192.168.1.106"],
    'port': 9001,
    "function": "actionDetection",
    'des_ip': '127.0.0.1'
}

computer3 = {
    'IP_list': ["192.168.1.107", "192.168.1.108", "192.168.1.109"],
    'port': 9002,
    "function": "faceDetection",
    'des_ip': '127.0.0.1'
}
computers={
    'computer1':computer1,
    'computer2':computer2,
    'computer3':computer3
}

def tcp_connection(computer):
    # 创建套接字
    des_socket = socket(AF_INET, SOCK_STREAM)
    ip=computer['des_ip']
    port=computer['port']
    des_socket.connect((ip, port))
    return des_socket


if __name__ == "__main__":
    for computer in computers:
        des_socket = tcp_connection(computer)
        computer['socket'] = des_socket

    # 本机socket
    local_socket = socket(AF_INET, SOCK_STREAM)
    address = ('127.0.0.1', 7000)
    local_socket.bind(address)
    #listen里的数字表征同一时刻能连接客户端的程度.
    local_socket.listen(128)

    while True:
        client_socket, clientAddr = local_socket.accept()
        data = client_socket.recv(1024).decode("utf-8")
        if data:
            data = json.loads(data)
            ip = data['cameraIP']
            function = data['function']
            for computer in computers:
                if ip in computer['IP_list'] and function==computer['function']:
                    computer['socket'].send(data.encode("utf-8"))
