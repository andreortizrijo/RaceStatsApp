import socket, threading, pickle

HEADER = 30
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
QUEUE = 5
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    
    while connected:
        full_msg = b''
        headerchek = True

        while True:
            msg = conn.recv(HEADER)

            if headerchek == True and msg.decode(FORMAT) != '':
                msg_length = int(msg[:HEADER])
                headerchek = False
            else:
                headerchek = False

            full_msg += msg

            if len(full_msg) == 0:
                break

            if len(full_msg) - HEADER == msg_length:
                full_msg = pickle.loads(full_msg[HEADER:])
                if full_msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f'[{addr}] Client disconnected')
                else:
                    print(f'[{addr}] {full_msg}')

                headerchek = True
                full_msg = b''

    conn.close()

def start():
    # If server get overload with info it will have a queue of n
    server.listen(QUEUE)
    print(f'[LISTENNIG] Server is running on {SERVER}')

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

print('Server is starting ...')
start()