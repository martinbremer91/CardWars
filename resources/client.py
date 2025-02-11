import socket
import sys

if len(sys.argv) != 3:
    print("the server ip and port must be passed in as system args")
    exit()

SERVER = sys.argv[1]

PORT = sys.argv[2]

if not PORT.isdigit():
    print("sys arg must be an integer")
    exit()

PORT = int(PORT)
print(f"[ADDRESS] {SERVER}/{PORT}")
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    print("sending...")
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

if PORT:
    send("Hello World!")
    send(DISCONNECT_MESSAGE)
else:
    print("invalid sys arg PORT")
