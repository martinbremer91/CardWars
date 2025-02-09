import socket
import threading
import urllib.request

wi_fi_connect : bool = False

ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
source_port = 50123 if not wi_fi_connect else 50128
destination_port = 50124 if not wi_fi_connect else 50129

socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_send.bind(('0.0.0.0', source_port))
socket_send.sendto(b'0', (ip, destination_port))

def listen():
    socket_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_listen.bind(('0.0.0.0', source_port))

    while True:
        data = socket_listen.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True)
listener.start()

socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_send.bind(('0.0.0.0', destination_port))

while True:
    msg = input('> ')
    socket_send.sendto(msg.encode(), (ip, source_port))
