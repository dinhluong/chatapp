from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5500
ADDR = (HOST, PORT)
BUFFSIZ =  512
# GLOBAL VARIABLES
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
messages = []

def receive_messages():
    while True:
        try:
            msg = client_socket.recv(BUFFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]",e)
            break

def send_messages(msg):
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()

receive_thread = Thread(target=receive_messages)
receive_thread.start()

send_messages("luong")
send_messages("hello")
send_messages("{quit}")