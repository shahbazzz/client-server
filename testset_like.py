import socket
import pickle
import time

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.160.238"
#SERVER = "192.168.1.12"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_message_to_pyipc_server(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    u = client.recv(2000).decode(FORMAT)
    print(u)
    return u

send_message_to_pyipc_server("abc")
time.sleep(10)
exit()
send_message_to_pyipc_server(f"!CONNECT**testset**portlist")
send_message_to_pyipc_server(f"!CMD**testset**portlist**puts \"cccc\"")
