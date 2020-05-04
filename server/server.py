from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person
HOST = 'localhost'
PORT = 5500
BUFFSIZ = 512
MAX_CONNECTION = 100
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


# GLOBAL VARIABERS
persons = []

def broadcast(msg, name):
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name + " : ", "utf8")+ msg)
        except Exception as e:
            print("[FAILURE]", e)

def client_communication(person):
    """
    Thread to handle all messages from clients
    :param client: person
    :return: none
    """
    client = person.client
    addr = person.addr

    # get person name
    name = client.recv(BUFFSIZ).decode("utf8")
    msg = bytes(f"{name} has join the chat","utf8")
    broadcast(msg, "")

    while True:
        try:
            msg = client.recv(BUFFSIZ)
            if msg == bytes("{quit}","utf8"):
                broadcast(f"{name} has left the chat ...", "")
                client.send("{quit}","utf8")
                client.close()
                persons.remove(person)
            else:
                broadcast(msg, name)
        except Exception as e:
            print("[FAILURE]", e)
            break
def wait_for_connection():
    """
    Wait for connection from client and Open new thread when new connection happend.
    :param SERVER
    :return: none
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]", e)
            run = False
    print("Server crashed")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTION) # listen for connection
    print("Waiting for connection")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()