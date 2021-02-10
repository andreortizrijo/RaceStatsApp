import socket
import threading

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:        
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'[{addr}] {msg}')
            
    conn.close()

def start():
    s.listen()
    print(f'[LISTENNIG] Server is running on {SERVER}')
    while True:
        client_socket, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

print('Server is starting ...')
start()