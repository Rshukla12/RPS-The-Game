import socket
from _thread import *


def win(client_state_1, client_state_2):
    user_in = int(client_state_1)
    option_no = int(client_state_2)

    if user_in == option_no:
        msg_1 = msg_2 = "Draw!!"
    elif (user_in == 0 and option_no == 2) or (user_in == 1 and option_no == 0)\
            or (user_in == 2 and option_no == 1):
        msg_1 = "LOST!!"
        msg_2 = "WON!!!"
    else:
        msg_1 = "WON!!!"
        msg_2 = "LOST!!"

    msg_1 += str(user_in) + str(option_no)
    msg_2 += str(option_no) + str(user_in)
    return msg_1, msg_2


def client_threading(conn, i):
    global clients
    while True:
        client = conn.recv(1024)
        if client:
            break
    clients[i] = client


# Declaring Constants
IP = "127.0.0.1"
PORT = 1234

# Starting Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen(2)

clients = {}

while True:

    # First client connection
    client_socket_1, address1 = server_socket.accept()
    print(f"connection from {address1} has been established")

    start_new_thread(client_threading, (client_socket_1, 1))

    # Second Client Connection
    client_socket_2, address2 = server_socket.accept()
    print(f"connection from {address2} has been established")

    start_new_thread(client_threading, (client_socket_2, 2))

    while len(clients) < 2:
        continue
    print(clients)
    client1 = clients[1].decode('utf-8')
    client2 = clients[2].decode('utf-8')

    msg1, msg2 = win(client1, client2)

    client_socket_1.send(bytes(msg1, 'utf-8'))
    client_socket_2.send(bytes(msg2, 'utf-8'))
