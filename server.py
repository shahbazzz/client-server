import socket
import pickle
import select
import threading
import pyipc_object_mapper as arx


interp = dict()
proc_var = dict()

# to make msg size constant
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# concurrently run
def handle_client(conn, addr):
    print(f"NEW Connection {addr} connected")
    connected = True
    while connected:
        # recieve the msg from server
        try:
            ready_to_read, ready_to_write, in_error = \
                select.select([conn, ], [conn, ], [], 5)
        except select.error:
            conn.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
            conn.close()
            # connection error event here, maybe reconnect
            print
            'connection error'
            break
        if len(ready_to_read) > 0:
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
            except Exception as e:
                print(str(e))
                connected = False
                break
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                proc_var[msg] = msg
                conn.send(f"Got it {msg}".encode(FORMAT))
                print(f"\ninterp: {proc_var}")

                if msg.startswith("!CONNECT"):
                    chunks = msg.split("**")
                    if len(chunks)<3:
                        conn.send(f"Send proper format. !CONNECT**testset**portlist".encode(FORMAT))
                        continue
                    key = f"{chunks[1]}//{chunks[2]}"
                    new = arx.RemoteTcl(chunks[1],chunks[2:])
                    interp[key] = new
                    conn.send(f"SUCCESS".encode(FORMAT))
                elif msg.startswith("!CMD"):
                    chunks = msg.split("**")
                    if len(chunks)<4:
                        conn.send(f"Send proper format. !CMD**testset**portlist++cmd".encode(FORMAT))
                        continue
                    key = f"{chunks[1]}//{chunks[2]}"
                    if key in interp.keys():
                        ret = interp[key].tcl_eval(chunks[3])
                        conn.send(f"{ret}".encode(FORMAT))
                    else:
                        conn.send(f"Corresponding interpreter not found".encode(FORMAT))
                elif msg == DISCONNECT_MESSAGE:
                    connected = False
                    conn.close()

# to start listening the connection
# and accept new connection
def start():
    # socket creation (Family , Type)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the server
    server.bind(ADDR)
    server.listen()
    print(f"LISTENING: {SERVER}")
    while True:
        # info about to connection in conn, addr
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\nACTIVE CONNECTION {threading.activeCount()-1}")

