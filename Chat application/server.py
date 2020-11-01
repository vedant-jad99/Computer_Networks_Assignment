#Chat application

import socket
import time
import threading

PORT = 8080
HOST = "192.168.0.105"
sock = None
conn_list = []
client_count = 1

def Create():
    try:
        global sock
        sock = socket.socket()
    except:
        print("Error creating socket")

def Bind():
    try:
        global sock
        print("Binding the port...")
        sock.bind((HOST, PORT))
        sock.listen(5)
    except socket.error as e:
        print(e)
        Bind()
    
def Listen():
    global conn_list, client_count
    while True:
        try:
            conn, addr = sock.accept()
            if conn != None:
                print("Connection to client successful.")
                conn_list.append((conn, addr, client_count))
                client_count += 1
                thread = threading.Thread(target=AcceptMessages, args=(conn, ))
                thread.start()
        except socket.error as e:
            print(e)

def SendToClient(conn):
    global conn_list
    for i in conn_list:
        message = str(i[2]) + " : " + str(i[1]) + "\n"
        conn.send(str.encode(message))
    conn.send(str.encode('over'))

def AcceptMessages(conn):
    while True:
        message = conn.recv(1024)
        message = message.decode("utf-8")
        if message == 'list()':
            SendToClient(conn)
        elif message == 'quit()':
            i = conn_list.index(conn)
            conn_list.remove(i)
            print(conn_list)
            conn.close()
            break


if __name__ == '__main__':
    Create()
    Bind()
    Listen()
    
